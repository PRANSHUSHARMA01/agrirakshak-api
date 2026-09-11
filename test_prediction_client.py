import io
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "agrirakshak" / "backend"))

from app.services.prediction_client import PredictionClient

def main():
    client = PredictionClient("http://127.0.0.1:8000", threshold=0.60)

    print("Checking prediction API health...")
    healthy = client.check_health()
    print("API Healthy:", healthy)

    # Generate synthetic leaf image
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 40, 180, 180), fill=(139, 69, 19))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    print("\nSending prediction request...")
    res = client.predict_image(img_bytes, filename="test_leaf.jpg")

    print("\nNormalized Prediction Result:")
    print("Success:", res.get("success"))
    print("Predicted Class:", res.get("predicted_class"))
    print("Confidence:", res.get("confidence"))
    print("Needs Expert Review:", res.get("needs_expert_review"))
    print("Raw Response:", res.get("raw_response"))

    if res.get("success"):
        print("\nStep 1 Verification SUCCESSFUL!")
    else:
        print("\nStep 1 Verification FAILED:", res.get("error"))

if __name__ == "__main__":
    main()
