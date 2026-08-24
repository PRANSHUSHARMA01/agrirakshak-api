import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "agrirakshak-mvp" / "backend"))

from app.database import SessionLocal
from app.services.rag_service import rag_service
from fastapi.testclient import TestClient
from app.main import app

def main():
    db = SessionLocal()
    try:
        print("Testing RAG service direct disease query ('01_Bacterial_leaf_blight')...")
        res1 = rag_service.query_by_disease(db, "01_Bacterial_leaf_blight")
        print("RAG Direct Match Found:", res1.get("found"))
        print("Title:", res1.get("title"))
        print("Recommended Actions Count:", len(res1.get("recommended_actions", [])))
        print("Sample Action:", res1.get("recommended_actions", [""])[0][:120])

        print("\nTesting RAG text search ('how to control fall armyworm in maize')...")
        res2 = rag_service.search_text_query(db, "how to control fall armyworm in maize")
        print("RAG Search Found:", res2.get("found"))
        print("Title:", res2.get("title"))

        print("\nTesting FastAPI POST /chat/message with knowledge_query intent...")
        client = TestClient(app)
        response = client.post(
            "/chat/message",
            data={
                "message": "What is the chemical treatment for bacterial leaf blight in rice?",
                "session_id": "sess_rag_test",
                "language": "en",
                "intent": "knowledge_query"
            }
        )

        print("HTTP Status:", response.status_code)
        resp_data = response.json()
        print("Response JSON:")
        print(resp_data)

        if response.status_code == 200 and resp_data.get("success"):
            print("\nStep 3 Verification SUCCESSFUL!")
        else:
            print("\nStep 3 Verification FAILED!")

    finally:
        db.close()

if __name__ == "__main__":
    main()
