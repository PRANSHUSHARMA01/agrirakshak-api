import random
import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.farmer_case import FarmerCase
from app.models.escalation_case import EscalationCase
from app.models.user import User
from app.routers.auth import get_password_hash

DEMO_LOCATIONS = [
    {"name": "Delhi NCR", "lat": 28.6139, "lon": 77.2090},
    {"name": "Meerut", "lat": 28.9845, "lon": 77.7064},
    {"name": "Ghaziabad", "lat": 28.6692, "lon": 77.4538},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Kanpur", "lat": 26.4499, "lon": 80.3319},
    {"name": "Agra", "lat": 27.1767, "lon": 78.0081},
    {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739},
]

DEMO_DISEASES = [
    ("Bacterial Leaf Blight", "Rice", 0.94, False),
    ("Rice Blast", "Rice", 0.88, False),
    ("Rice Skipper", "Rice", 0.52, True),
    ("White Stem Borer", "Rice", 0.48, True),
    ("Brown Spot", "Rice", 0.76, False),
    ("Turcicum Leaf Blight", "Maize", 0.82, False),
    ("Fall Armyworm", "Maize", 0.55, True),
    ("Maize Common Rust", "Maize", 0.91, False),
]

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Seed officer user if not present
        user = db.query(User).filter(User.username == "officer").first()
        if not user:
            user = User(
                username="officer",
                email="officer@agrirakshak.gov.in",
                hashed_password=get_password_hash("officer123"),
                role="officer",
                full_name="Demo Agricultural Extension Officer"
            )
            db.add(user)
            db.commit()

        # Seed 15 realistic cases
        print("Seeding demo cases...")
        for i in range(15):
            loc = random.choice(DEMO_LOCATIONS)
            dis, crop, conf, needs_esc = random.choice(DEMO_DISEASES)
            days_ago = random.randint(0, 10)
            created_at = datetime.datetime.utcnow() - datetime.timedelta(days=days_ago)

            case = FarmerCase(
                session_id=f"demo-session-{i+1}",
                image_url=f"leaf_demo_{i+1}.jpg",
                crop=crop,
                predicted_class=dis,
                confidence=conf,
                latitude=loc["lat"],
                longitude=loc["lon"],
                location_name=loc["name"],
                status="escalated" if needs_esc else "diagnosed",
                needs_expert_review=needs_esc,
                created_at=created_at
            )
            db.add(case)
            db.commit()
            db.refresh(case)

            if needs_esc:
                escalation = EscalationCase(
                    farmer_case_id=case.id,
                    reason=f"Low confidence detection ({int(conf*100)}% < 60%)",
                    status="pending",
                    created_at=created_at
                )
                db.add(escalation)
                db.commit()

        print("Successfully seeded demo data for officer dashboard.")
    except Exception as e:
        print(f"Error seeding demo data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
