import os
import io
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
import numpy as np

PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "https://agrirakshak-model.onrender.com").rstrip("/")
PREDICTION_CONFIDENCE_THRESHOLD = float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", "0.60"))

# In-process model fallback initialization
_in_process_model = None
_in_process_interpreter = None
_in_process_use_tflite = False
_in_process_class_names = []
_in_process_loaded = False

def _init_in_process_model():
    global _in_process_model, _in_process_interpreter, _in_process_use_tflite, _in_process_class_names, _in_process_loaded
    if _in_process_loaded:
        return True

    try:
        current_file = Path(__file__).resolve()
        search_dirs = [
            Path("C:/Users/prans/OneDrive/Desktop/agrirakshak-api"),
            current_file.parent.parent.parent.parent,
            current_file.parent.parent.parent,
            Path.cwd(),
        ]
        
        tflite_path = None
        keras_path = None
        class_path = None

        for d in search_dirs:
            tp = d / "best_agri_finetuned.tflite"
            kp = d / "best_agri_finetuned.keras"
            cp = d / "class_names.json"
            if tp.exists() and not tflite_path:
                tflite_path = tp
            if kp.exists() and not keras_path:
                keras_path = kp
            if cp.exists() and not class_path:
                class_path = cp

        if class_path and class_path.exists():
            try:
                with open(class_path, "r", encoding="utf-8") as f:
                    _in_process_class_names = json.load(f)
            except Exception as e:
                print(f"[PredictionClient] Error loading class names: {e}")

        # 1. Try loading lightweight TFLite model first
        if tflite_path and tflite_path.exists():
            interpreter_cls = None
            for mod_name in ["ai_edge_litert.interpreter", "tflite_runtime.interpreter", "tensorflow.lite"]:
                try:
                    mod = __import__(mod_name, fromlist=["Interpreter"])
                    interpreter_cls = getattr(mod, "Interpreter")
                    break
                except Exception:
                    pass

            if interpreter_cls:
                try:
                    print(f"[PredictionClient] Loading in-process TFLite model from '{tflite_path}'...")
                    _in_process_interpreter = interpreter_cls(model_path=str(tflite_path))
                    _in_process_interpreter.allocate_tensors()
                    _in_process_use_tflite = True
                    _in_process_loaded = True
                    print("[PredictionClient] In-process TFLite model loaded successfully!")
                    return True
                except Exception as e:
                    print(f"[PredictionClient] TFLite load error: {e}")

        # 2. Fallback to Keras model if TFLite unavailable
        if keras_path and keras_path.exists():
            try:
                import keras
                print(f"[PredictionClient] Loading in-process Keras model from '{keras_path}'...")
                _in_process_model = keras.models.load_model(str(keras_path))
                _in_process_use_tflite = False
                _in_process_loaded = True
                print("[PredictionClient] In-process Keras model loaded successfully!")
                return True
            except Exception as e:
                print(f"[PredictionClient] In-process Keras model load error: {e}")

    except Exception as e:
        print(f"[PredictionClient] In-process model load warning: {e}")
    
    return False

class PredictionClient:
    """
    HTTP client wrapper for AgriRakshak prediction service with automatic in-process TFLite/Keras model fallback.
    """

    def __init__(self, base_url: Optional[str] = None, threshold: Optional[float] = None):
        self.base_url = (base_url or PREDICTION_API_URL).rstrip("/")
        self.threshold = threshold if threshold is not None else PREDICTION_CONFIDENCE_THRESHOLD

    def check_health(self) -> Dict[str, Any]:
        """
        Check health status of prediction service (HTTP endpoint or in-process model).
        """
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        is_proc = _init_in_process_model()
        return {
            "status": "ok" if is_proc else "degraded",
            "in_process_model_loaded": is_proc,
            "classes": len(_in_process_class_names)
        }

    def predict_in_process(self, image_bytes: bytes) -> Optional[Dict[str, Any]]:
        """
        Runs image inference in-process using TFLite or Keras model if available.
        """
        try:
            if not _init_in_process_model():
                return None

            image_raw = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image = image_raw.resize((224, 224))
            img_array = np.array(image, dtype=np.float32)
            img_array = np.expand_dims(img_array, axis=0)

            if _in_process_use_tflite and _in_process_interpreter is not None:
                input_details = _in_process_interpreter.get_input_details()
                output_details = _in_process_interpreter.get_output_details()
                _in_process_interpreter.set_tensor(input_details[0]['index'], img_array)
                _in_process_interpreter.invoke()
                predictions = _in_process_interpreter.get_tensor(output_details[0]['index'])
            elif _in_process_model is not None:
                predictions = _in_process_model.predict(img_array, verbose=0)
            else:
                return None

            scores = predictions[0]

            top_index = int(np.argmax(scores))
            confidence = float(scores[top_index])
            predicted_class = (
                _in_process_class_names[top_index]
                if top_index < len(_in_process_class_names)
                else f"Class_{top_index}"
            )

            top_3_indices = np.argsort(scores)[::-1][:3]
            top_predictions = [
                {
                    "class": _in_process_class_names[idx] if idx < len(_in_process_class_names) else f"Class_{idx}",
                    "confidence": round(float(scores[idx]), 4)
                }
                for idx in top_3_indices
            ]

            conf_normalized = round(confidence, 4) if confidence <= 1.0 else round(confidence / 100.0, 4)
            needs_expert = conf_normalized < self.threshold

            return {
                "success": True,
                "predicted_class": predicted_class,
                "confidence": conf_normalized,
                "needs_expert_review": needs_expert,
                "raw_response": {
                    "success": True,
                    "predicted_class": predicted_class,
                    "confidence": conf_normalized,
                    "top_predictions": top_predictions
                }
            }
        except Exception as e:
            print(f"[PredictionClient] In-process inference error: {e}")
            return None

    def predict_image(self, image_bytes: bytes, filename: str = "leaf.jpg") -> Dict[str, Any]:
        """
        Sends image to POST /predict microservice, and falls back to in-process TFLite/Keras inference seamlessly.
        """
        endpoint = f"{self.base_url}/predict"
        files = {"file": (filename, image_bytes, "image/jpeg")}

        # 1. Try external HTTP microservice with 35.0s timeout (accommodates Render free tier cold starts)
        try:
            resp = requests.post(endpoint, files=files, timeout=35.0)
            if resp.status_code == 200:
                raw_data = resp.json()
                if raw_data.get("success", False):
                    predicted_class = raw_data.get("predicted_class") or raw_data.get("prediction", "Unknown")
                    confidence = float(raw_data.get("confidence", 0.0))
                    conf_normalized = round(confidence, 4) if confidence <= 1.0 else round(confidence / 100.0, 4)
                    needs_expert = conf_normalized < self.threshold

                    return {
                        "success": True,
                        "predicted_class": predicted_class,
                        "confidence": conf_normalized,
                        "needs_expert_review": needs_expert,
                        "raw_response": raw_data
                    }
                else:
                    # Microservice rejected as non-crop image
                    return {
                        "success": False,
                        "is_crop_photo": False,
                        "predicted_class": raw_data.get("predicted_class", "Invalid Non-Crop Photo"),
                        "confidence": 0.0,
                        "needs_expert_review": False,
                        "fallback_message": raw_data.get("error", "Kindly upload a clear photo of a crop or plant leaf."),
                        "raw_response": raw_data
                    }
        except Exception as e:
            print(f"[PredictionClient] Microservice endpoint ({endpoint}) unavailable ({e}). Running in-process inference...")

        # 2. Fallback to in-process TFLite / Keras model
        in_proc_res = self.predict_in_process(image_bytes)
        if in_proc_res:
            return in_proc_res

        # 3. Final safety fallback
        return {
            "success": False,
            "predicted_class": "Unknown",
            "confidence": 0.0,
            "needs_expert_review": True,
            "fallback_message": "I couldn't process that image right now. Please try again or describe the symptoms."
        }

# Singleton instance
prediction_client = PredictionClient()
