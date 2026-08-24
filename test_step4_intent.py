import io
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "agrirakshak-mvp" / "backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.schema import FarmerCase, EscalationCase

def main():
    client = TestClient(app)

    print("--- 1. Testing image_diagnosis intent ---")
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 40, 180, 180), fill=(139, 69, 19))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    response1 = client.post(
        "/chat/message",
        data={
            "message": "Check my rice leaf for disease",
            "session_id": "sess_img_test",
            "language": "en",
            "latitude": 28.6139,
            "longitude": 77.2090
        },
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}
    )
    print("HTTP Status:", response1.status_code)
    r1 = response1.json()
    print("Intent:", r1.get("intent"))
    print("Predicted Class:", r1.get("response", {}).get("predicted_class"))
    print("Confidence:", r1.get("response", {}).get("confidence"))
    print("Needs Expert Review:", r1.get("response", {}).get("needs_expert_review"))
    print("Case ID:", r1.get("case_id"))

    print("\n--- 2. Testing knowledge_query intent ---")
    response2 = client.post(
        "/chat/message",
        data={
            "message": "How to treat bacterial leaf blight in rice?",
            "session_id": "sess_kq_test",
            "language": "en"
        }
    )
    print("HTTP Status:", response2.status_code)
    r2 = response2.json()
    print("Intent:", r2.get("intent"))
    print("Diagnosis/Answer:", r2.get("response", {}).get("diagnosis_or_answer")[:100])

    print("\n--- 3. Testing weather_risk intent ---")
    response3 = client.post(
        "/chat/message",
        data={
            "message": "Is there rain forecast for monsoon in my area?",
            "session_id": "sess_wr_test",
            "language": "en"
        }
    )
    print("HTTP Status:", response3.status_code)
    r3 = response3.json()
    print("Intent:", r3.get("intent"))

    print("\n--- 4. Testing general intent fallback ---")
    response4 = client.post(
        "/chat/message",
        data={
            "message": "What is the capital of France?",
            "session_id": "sess_gen_test",
            "language": "en"
        }
    )
    print("HTTP Status:", response4.status_code)
    r4 = response4.json()
    print("Intent:", r4.get("intent"))
    print("Restricted Answer:", r4.get("response", {}).get("diagnosis_or_answer"))

    # Verify DB persistence
    db = SessionLocal()
    try:
        cases_count = db.query(FarmerCase).count()
        print(f"\nTotal FarmerCase records in DB: {cases_count}")
        if response1.status_code == 200 and r1.get("success") and cases_count > 0:
            print("Step 4 Verification SUCCESSFUL!")
        else:
            print("Step 4 Verification FAILED!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
