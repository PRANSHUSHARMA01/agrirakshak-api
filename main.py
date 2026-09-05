import io
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np

# Use keras directly for Keras 3 model compatibility
import keras

# ============================================================
# PATHS AND CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_agri_finetuned.keras"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"
IMG_SIZE = (224, 224)

# Ensure backend directory is in sys.path to load routers
backend_dir = BASE_DIR / "agrirakshak" / "backend"
if backend_dir.exists() and str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.crop_validator import validate_crop_image

# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="AgriRakshak AI API",
    description="Crop disease detection API using fine-tuned Keras model and Officer Console API",
    version="1.0.0"
)

# CORS configuration for Next.js frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount AgriRakshak Core Routers (Auth, Dashboard, Reports, Chat, Weather)
try:
    from app.routers import health as h_router, auth, prediction, chat, weather, reports, dashboard
    app.include_router(auth.router)
    app.include_router(prediction.router)
    app.include_router(chat.router)
    app.include_router(weather.router)
    app.include_router(reports.router)
    app.include_router(dashboard.router)
    print("ALL AGRIRAKSHAK ROUTERS (AUTH, DASHBOARD, REPORTS, CHAT) MOUNTED SUCCESSFULLY!")
except Exception as e:
    print(f"Warning mounting backend routers in root main.py: {e}")

# Global variables for loaded resources
model = None
class_names = []
model_loaded = False

# ============================================================
# RESOURCE LOADING
# ============================================================

def load_resources():
    global model, class_names, model_loaded

    # Load Model using absolute/project-relative path
    if MODEL_PATH.exists():
        try:
            print(f"Loading AgriRakshak model from '{MODEL_PATH}'...")
            model = keras.models.load_model(str(MODEL_PATH))
            model_loaded = True
            print("MODEL LOADED SUCCESSFULLY")
        except Exception as e:
            print(f"Error loading model from '{MODEL_PATH}': {e}")
            model_loaded = False
    else:
            print(f"WARNING: Model file '{MODEL_PATH}' not found.")
            model_loaded = False

    # Load Class Names using absolute/project-relative path
    if CLASS_NAMES_PATH.exists():
        try:
            print(f"Loading class names from '{CLASS_NAMES_PATH}'...")
            with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
                class_names = json.load(f)
            print(f"CLASS COUNT: {len(class_names)}")
        except Exception as e:
            print(f"Error loading class names: {e}")
            class_names = []
    else:
        print(f"WARNING: Class names file '{CLASS_NAMES_PATH}' not found.")

# Load resources once when application starts
load_resources()

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def home() -> Dict[str, Any]:
    return {
        "name": "AgriRakshak AI API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
def health() -> Dict[str, Any]:
    is_healthy = model_loaded and len(class_names) == 32
    return {
        "status": "ok" if is_healthy else "degraded",
        "model_loaded": model_loaded,
        "classes": len(class_names)
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> JSONResponse:
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded."
        )

    if not class_names:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Class names are not loaded."
        )

    if file.content_type and not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": "Uploaded file is not an image."
            }
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": "Invalid or unreadable image file."
            }
        )

    # Validate if uploaded image is a valid crop/leaf photo
    is_valid, validation_msg = validate_crop_image(image)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": False,
                "is_crop_photo": False,
                "error": validation_msg,
                "predicted_class": "Invalid Non-Crop Photo",
                "prediction": "Invalid Non-Crop Photo",
                "confidence": 0.0
            }
        )

    image_resized = image.resize(IMG_SIZE)
    img_array = np.array(image_resized, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)

    try:
        predictions = model.predict(img_array, verbose=0)
        scores = predictions[0]

        top_index = int(np.argmax(scores))
        confidence = float(scores[top_index])
        predicted_class = (
            class_names[top_index]
            if top_index < len(class_names)
            else f"Class_{top_index}"
        )

        top_3_indices = np.argsort(scores)[::-1][:3]
        top_predictions = [
            {
                "class": class_names[idx] if idx < len(class_names) else f"Class_{idx}",
                "confidence": round(float(scores[idx]), 4)
            }
            for idx in top_3_indices
        ]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "predicted_class": predicted_class,
                "prediction": predicted_class,
                "confidence": round(confidence, 4),
                "class_index": top_index,
                "top_predictions": top_predictions
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": f"Prediction failed: {str(e)}"
            }
        )