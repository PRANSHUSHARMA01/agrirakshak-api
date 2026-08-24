import os
import re
import json
from pathlib import Path
from app.database import engine, SessionLocal, Base
from app.models.schema import KnowledgeDocument

KB_DIR = Path(__file__).resolve().parent / "app" / "knowledge_base"
# Point to root class_names.json
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CLASS_NAMES_PATH = ROOT_DIR / "class_names.json"

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if not CLASS_NAMES_PATH.exists():
            print(f"Error: {CLASS_NAMES_PATH} not found.")
            return

        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            class_names = json.load(f)

        print(f"Loaded {len(class_names)} target class names.")

        md_files = list(KB_DIR.glob("*.md"))
        print(f"Found {len(md_files)} knowledge base markdown files.")

        documents_added = 0

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            sections = content.split("## ")
            
            for section in sections[1:]:
                header = section.split("\n")[0].strip()
                
                # Match disease class from class_names
                matched_class = None
                for c in class_names:
                    if c in header or c.lower() in header.lower():
                        matched_class = c
                        break
                
                if not matched_class:
                    continue

                # Parse subsections
                symptoms = ""
                cultural = ""
                biological = ""
                chemical = ""

                if "### Symptoms" in section:
                    symptoms = section.split("### Symptoms")[1].split("###")[0].strip()
                if "### Cultural Control" in section:
                    cultural = section.split("### Cultural Control")[1].split("###")[0].strip()
                if "### Biological Control" in section:
                    biological = section.split("### Biological Control")[1].split("###")[0].strip()
                if "### Chemical Control" in section or "### Control" in section:
                    parts = section.split("### Chemical Control") if "### Chemical Control" in section else section.split("### Control")
                    chemical = parts[1].split("###")[0].strip()

                # Upsert into DB
                existing = db.query(KnowledgeDocument).filter(KnowledgeDocument.disease_class == matched_class).first()
                if existing:
                    existing.title = header
                    existing.content = section
                    existing.symptoms = symptoms
                    existing.cultural_control = cultural
                    existing.biological_control = biological
                    existing.chemical_control = chemical
                else:
                    doc = KnowledgeDocument(
                        disease_class=matched_class,
                        title=header,
                        content=section,
                        symptoms=symptoms,
                        cultural_control=cultural,
                        biological_control=biological,
                        chemical_control=chemical
                    )
                    db.add(doc)
                    documents_added += 1

        db.commit()
        total_docs = db.query(KnowledgeDocument).count()
        print(f"Seeding complete! Added {documents_added} new documents. Total in DB: {total_docs}")

    except Exception as e:
        db.rollback()
        print(f"Seeding error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
