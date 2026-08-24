import re
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.schema import KnowledgeDocument

class RAGService:
    """
    RAG & Knowledge Base Retrieval Service.
    Retrieves curated IPDM practices, symptoms, controls, and PHI safety guidance.
    Strictly prevents hallucinated chemical dosages by defaulting to Krishi Vigyan Kendra referral.
    """

    def query_by_disease(self, db: Session, disease_class: str) -> Dict[str, Any]:
        """
        Query knowledge base by exact or partial disease class name.
        """
        doc = db.query(KnowledgeDocument).filter(
            KnowledgeDocument.disease_class == disease_class
        ).first()

        if not doc:
            # Fallback search by partial keyword match
            doc = db.query(KnowledgeDocument).filter(
                KnowledgeDocument.title.ilike(f"%{disease_class}%")
            ).first()

        if doc:
            recommended_actions = []
            if doc.cultural_control:
                recommended_actions.append(f"Cultural Control: {doc.cultural_control[:200]}")
            if doc.biological_control:
                recommended_actions.append(f"Biological Control: {doc.biological_control[:200]}")
            if doc.chemical_control:
                recommended_actions.append(f"Chemical Control & Safe Dosage: {doc.chemical_control[:250]}")

            return {
                "found": True,
                "disease_class": doc.disease_class,
                "title": doc.title,
                "symptoms": doc.symptoms or "Consult local extension officer for detailed symptoms.",
                "cultural_control": doc.cultural_control or "Ensure balanced nutrition and good field sanitation.",
                "biological_control": doc.biological_control or "Apply recommended bio-agents (e.g. Trichoderma or Pseudomonas).",
                "chemical_control": doc.chemical_control or "Consult your local Krishi Vigyan Kendra / extension officer for verified chemical recommendations.",
                "recommended_actions": recommended_actions or ["Consult your local Krishi Vigyan Kendra / extension officer."],
                "safety_notes": "Always wear protective gear (mask, gloves) when handling plant protection products. Follow Pre-Harvest Intervals (PHI) carefully."
            }

        # Fallback when disease context is not found
        return {
            "found": False,
            "disease_class": disease_class,
            "title": f"Advisory for {disease_class}",
            "symptoms": "Information for this specific disease is being updated.",
            "recommended_actions": [
                "Isolate infected plant parts to prevent field spread.",
                "Maintain proper drainage and avoid leaf wetness.",
                "Consult your local Krishi Vigyan Kendra / agricultural extension officer for verified local treatment."
            ],
            "safety_notes": "Do not apply unknown chemical pesticides without official agricultural extension advice."
        }

    def search_text_query(self, db: Session, query: str) -> Dict[str, Any]:
        """
        Search knowledge base using text query keywords.
        """
        query_clean = query.lower()
        docs = db.query(KnowledgeDocument).all()

        best_doc = None
        best_score = 0

        for doc in docs:
            score = 0
            keywords = re.findall(r'\w+', doc.content.lower())
            for kw in set(keywords):
                if len(kw) > 3 and kw in query_clean:
                    score += 1
            if score > best_score:
                best_score = score
                best_doc = doc

        if best_doc and best_score >= 1:
            return self.query_by_disease(db, best_doc.disease_class)

        # Restricted default response if no context matches
        return {
            "found": False,
            "query": query,
            "answer": "I'm not sure based on my curated knowledge base. Please consult your local Krishi Vigyan Kendra (KVK) or agricultural extension officer rather than guessing treatments.",
            "recommended_actions": [
                "Take clear photos of the infected leaf margins or fruit spots.",
                "Visit your nearest Krishi Vigyan Kendra (KVK) or block agricultural office."
            ],
            "safety_notes": "Avoid unverified chemical applications."
        }

rag_service = RAGService()
