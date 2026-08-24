import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.intent_classifier import intent_classifier
from app.services.prediction_client import prediction_client
from app.services.rag_service import rag_service
from app.models.schema import FarmerCase, EscalationCase

router = APIRouter(prefix="/chat", tags=["Chat & Advisory"])

@router.post("/message")
async def chat_message(
    message: Optional[str] = Form(None),
    session_id: Optional[str] = Form("default_session"),
    language: Optional[str] = Form("en"),
    intent: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    crop_type: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Main Farmer Chatbot Endpoint.
    Routes requests by intent:
    - image_diagnosis -> prediction_client -> FarmerCase DB -> EscalationCase if needed
    - knowledge_query -> RAG knowledge base lookup
    - weather_risk -> weather risk assessment
    - general -> LLM fallback restricted to agricultural queries
    """

    has_image = file is not None
    detected_intent = intent_classifier.classify(message=message, has_image=has_image, explicit_intent=intent)

    # ============================================================
    # BRANCH 1: IMAGE DIAGNOSIS
    # ============================================================
    if detected_intent == "image_diagnosis":
        if not file:
            return {
                "success": False,
                "session_id": session_id,
                "intent": "image_diagnosis",
                "error": "No image uploaded. Please upload a clear photo of the crop leaf.",
                "response": {
                    "diagnosis_or_answer": "Please attach an image of the affected crop leaf or describe the symptoms.",
                    "recommended_actions": ["Upload a clear leaf photo."],
                    "safety_notes": "Avoid spraying chemicals without positive diagnosis.",
                    "escalation_flag": False
                }
            }

        img_bytes = await file.read()
        pred_res = prediction_client.predict_image(img_bytes, filename=file.filename or "leaf.jpg")

        if not pred_res.get("success", False):
            return {
                "success": False,
                "session_id": session_id,
                "intent": "image_diagnosis",
                "error": pred_res.get("error"),
                "response": {
                    "diagnosis_or_answer": pred_res.get("fallback_message", "I couldn't process that image, please try again or describe the symptoms instead."),
                    "recommended_actions": ["Try taking a clearer, well-lit photo of the single leaf."],
                    "safety_notes": "Avoid unverified chemical applications.",
                    "escalation_flag": True
                }
            }

        predicted_class = pred_res.get("predicted_class")
        confidence = pred_res.get("confidence", 0.0)
        needs_expert_review = pred_res.get("needs_expert_review", False)

        # 1. Persist FarmerCase to DB
        case = FarmerCase(
            session_id=session_id,
            image_url=file.filename or "uploaded_leaf.jpg",
            predicted_class=predicted_class,
            confidence=confidence,
            needs_expert_review=needs_expert_review,
            latitude=latitude,
            longitude=longitude,
            crop_type=crop_type,
            user_query=message
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        # 2. If needs_expert_review is True, create EscalationCase
        escalation_id = None
        if needs_expert_review:
            esc = EscalationCase(
                case_id=case.id,
                status="pending"
            )
            db.add(esc)
            db.commit()
            db.refresh(esc)
            escalation_id = esc.id

        # 3. Retrieve RAG advisory for the predicted disease
        rag_info = rag_service.query_by_disease(db, predicted_class)
        recommended_actions = rag_info.get("recommended_actions", [])

        if needs_expert_review:
            recommended_actions.insert(0, "Your case has low prediction confidence and has been flagged for Expert Review.")

        return {
            "success": True,
            "session_id": session_id,
            "intent": "image_diagnosis",
            "case_id": case.id,
            "language": language,
            "response": {
                "diagnosis_or_answer": f"Predicted Disease: {predicted_class} (Confidence: {round(confidence * 100, 1)}%)",
                "predicted_class": predicted_class,
                "confidence": confidence,
                "needs_expert_review": needs_expert_review,
                "escalation_id": escalation_id,
                "recommended_actions": recommended_actions,
                "safety_notes": rag_info.get("safety_notes", "Follow safety precautions when handling chemical sprays."),
                "escalation_flag": needs_expert_review
            }
        }

    # ============================================================
    # BRANCH 2: KNOWLEDGE QUERY
    # ============================================================
    if detected_intent == "knowledge_query":
        query_text = message or "crop disease control"
        rag_res = rag_service.search_text_query(db, query_text)

        answer = rag_res.get("answer") or rag_res.get("symptoms", "")
        recommended_actions = rag_res.get("recommended_actions", [])
        safety_notes = rag_res.get("safety_notes", "Consult extension officer for verified treatments.")

        if language == "hi":
            answer = f"[हिंदी] {answer}"
            safety_notes = "कीटनाशक का प्रयोग करते समय हमेशा मास्क और दस्ताने पहनें।"

        return {
            "success": True,
            "session_id": session_id,
            "intent": "knowledge_query",
            "language": language,
            "response": {
                "diagnosis_or_answer": answer,
                "recommended_actions": recommended_actions,
                "safety_notes": safety_notes,
                "escalation_flag": False
            }
        }

    # ============================================================
    # BRANCH 3: WEATHER RISK
    # ============================================================
    if detected_intent == "weather_risk":
        return {
            "success": True,
            "session_id": session_id,
            "intent": "weather_risk",
            "language": language,
            "response": {
                "diagnosis_or_answer": "Weather risk assessment for your region.",
                "recommended_actions": ["Check the Weather Risk endpoint for detailed forecast rules."],
                "safety_notes": "Avoid chemical spraying during strong winds or incoming rain.",
                "escalation_flag": False
            }
        }

    # ============================================================
    # BRANCH 4: GENERAL / RESTRICTED FALLBACK
    # ============================================================
    return {
        "success": True,
        "session_id": session_id,
        "intent": "general",
        "language": language,
        "response": {
            "diagnosis_or_answer": "I am specialized in crop disease detection and pest management. For unverified general topics, I'm not sure, please consult your local Krishi Vigyan Kendra (KVK) or extension officer.",
            "recommended_actions": [
                "Ask a question about crop symptoms or pest control.",
                "Upload a photo of your affected crop leaf.",
                "Contact your local Krishi Vigyan Kendra (KVK)."
            ],
            "safety_notes": "Always consult agricultural authorities before applying unverified practices.",
            "escalation_flag": False
        }
    }
