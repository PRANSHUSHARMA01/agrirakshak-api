import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "agrirakshak-mvp" / "backend"))

from app.database import engine, SessionLocal, Base
from app.models.schema import FarmerCase, EscalationCase, Expert

def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Create test FarmerCase
        case = FarmerCase(
            session_id="sess_test_123",
            image_url="http://127.0.0.1:8000/uploads/test.jpg",
            predicted_class="07_White_stem_borer",
            confidence=0.9849,
            needs_expert_review=False,
            latitude=28.6139,
            longitude=77.2090,
            crop_type="Rice",
            region="North India",
            user_query="My rice crop leaves are yellowing with stem borer symptoms."
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        print(f"Persisted FarmerCase successfully! ID: {case.id}")

        # Retrieve case
        retrieved = db.query(FarmerCase).filter(FarmerCase.id == case.id).first()
        print("Retrieved Case:")
        print(" - ID:", retrieved.id)
        print(" - Session ID:", retrieved.session_id)
        print(" - Predicted Class:", retrieved.predicted_class)
        print(" - Confidence:", retrieved.confidence)
        print(" - Needs Expert Review:", retrieved.needs_expert_review)
        print(" - Lat/Long:", retrieved.latitude, retrieved.longitude)

        if retrieved and retrieved.predicted_class == "07_White_stem_borer":
            print("\nStep 2 Verification SUCCESSFUL!")
        else:
            print("\nStep 2 Verification FAILED!")

    finally:
        db.close()

if __name__ == "__main__":
    main()
