import io
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw

# Add agrirakshak/backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "agrirakshak" / "backend"))

from app.services.prediction_client import PredictionClient

def main():
    client = PredictionClient("http://127.0.0.1:8000", threshold=0.60)

    print("Checking prediction API health...")
    health = client.check_health()
    print("Health response:", health)

    # Fetch OpenAPI spec to confirm schema detected
    print("\nFetching openapi.json...")
    spec = client.get_openapi_spec()
    predict_schema = spec.get("paths", {}).get("/predict", {})
    print("Detected /predict schema operationId:", predict_schema.get("post", {}).get("operationId"))

    # Generate synthetic crop leaf image
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 40, 180, 180), fill=(139, 69, 19))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    print("\nExecuting prediction request...")
    res = client.predict_image(img_bytes, filename="sample_crop_leaf.jpg")

    print("\nNormalized Prediction Result:")
    print(json.dumps(res, indent=2))

    print("\nSTEP 1 VERIFICATION RESULT:")
    print("Prediction API URL:", client.base_url)
    print("Health Status:", health.get("status"))
    print("Predicted Class:", res.get("predicted_class"))
    print("Confidence:", res.get("confidence"))
    print("Needs Expert Review:", res.get("needs_expert_review"))

if __name__ == "__main__":
    main()
