import base64
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.intent_classifier import classify_intent
from app.services.prediction_client import prediction_client
from app.services.advisory_service import generate_advisory
from app.services.escalation_service import create_escalation
from app.services.rag_service import query_rag
from app.services.translation_service import translate_advisory
from app.routers.weather import get_weather_risk
from app.models.farmer_case import FarmerCase
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, AdvisoryResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message", response_model=ChatMessageResponse)
def handle_chat_message(payload: ChatMessageRequest, db: Session = Depends(get_db)):
    """
    Main entrypoint for AgriRakshak farmer interactions.
    Dynamically routes queries and returns structured advisory localized in specified language.
    """
    has_image = bool(payload.image_base64)
    intent = classify_intent(payload.message or "", has_image=has_image)
    lang = (payload.language or "en").lower()

    # INTENT 1: IMAGE DIAGNOSIS
    if intent == "image_diagnosis" or has_image:
        if payload.image_base64:
            try:
                image_data = payload.image_base64
                if "," in image_data:
                    image_data = image_data.split(",")[1]
                image_bytes = base64.b64decode(image_data)
            except Exception:
                advisory = AdvisoryResponse(
                    diagnosis_or_answer="I couldn't process that image right now. Please try again or describe the symptoms.",
                    recommended_actions=["Upload a clear photo of the affected crop leaf."],
                    safety_notes=["Ensure the photo is well-lit and in focus."],
                    escalation_flag=False
                )
                return ChatMessageResponse(
                    intent="image_diagnosis",
                    session_id=payload.session_id,
                    advisory=translate_advisory(advisory, lang)
                )

            pred_res = prediction_client.predict_image(image_bytes, filename="leaf_upload.jpg")

            if not pred_res.get("success"):
                fallback_msg = pred_res.get(
                    "fallback_message",
                    "I couldn't process that image right now. Please try again or describe the symptoms."
                )
                advisory = AdvisoryResponse(
                    diagnosis_or_answer=fallback_msg,
                    recommended_actions=["Upload a clear photo of the affected crop leaf or describe the visible symptoms."],
                    safety_notes=["Consult your local agricultural office if symptoms persist."],
                    escalation_flag=False
                )
                return ChatMessageResponse(
                    intent="image_diagnosis",
                    session_id=payload.session_id,
                    advisory=translate_advisory(advisory, lang),
                    prediction_result=pred_res
                )

            predicted_class = pred_res.get("predicted_class", "Unknown")
            confidence = pred_res.get("confidence", 0.0)
            needs_expert = pred_res.get("needs_expert_review", False)

            # Save FarmerCase to DB
            farmer_case = FarmerCase(
                session_id=payload.session_id,
                crop=payload.crop or "Rice",
                predicted_class=predicted_class,
                confidence=confidence,
                latitude=payload.latitude or 28.6139,
                longitude=payload.longitude or 77.2090,
                status="diagnosed",
                needs_expert_review=needs_expert,
                raw_prediction=json.dumps(pred_res.get("raw_response", {}))
            )
            db.add(farmer_case)
            db.commit()
            db.refresh(farmer_case)

            if needs_expert:
                create_escalation(
                    db=db,
                    farmer_case_id=farmer_case.id,
                    reason=f"Low confidence detection ({int(confidence*100)}% < 60%)"
                )

            raw_advisory = generate_advisory(predicted_class, confidence, needs_expert)

            return ChatMessageResponse(
                intent="image_diagnosis",
                session_id=payload.session_id,
                advisory=translate_advisory(raw_advisory, lang),
                prediction_result=pred_res,
                farmer_case_id=farmer_case.id
            )
        else:
            advisory = AdvisoryResponse(
                diagnosis_or_answer="Please upload or capture a crop leaf image for AgriRakshak to analyze.",
                recommended_actions=["Tap 'Scan Crop' to attach an image."],
                safety_notes=["Take photos under bright, natural daylight."],
                escalation_flag=False
            )
            return ChatMessageResponse(
                intent="image_diagnosis",
                session_id=payload.session_id,
                advisory=translate_advisory(advisory, lang)
            )

    # INTENT 2: KNOWLEDGE QUERY (RAG)
    if intent == "knowledge_query":
        raw_advisory = query_rag(payload.message or "", crop=payload.crop)
        return ChatMessageResponse(
            intent="knowledge_query",
            session_id=payload.session_id,
            advisory=translate_advisory(raw_advisory, lang)
        )

    # INTENT 3: WEATHER RISK
    if intent == "weather_risk":
        lat = payload.latitude or 28.6139
        lon = payload.longitude or 77.2090
        crop = payload.crop or "Rice"
        w_res = get_weather_risk(latitude=lat, longitude=lon, crop=crop)

        raw_advisory = AdvisoryResponse(
            diagnosis_or_answer=f"Weather Risk Assessment ({crop}): Level {w_res.risk_level}. {w_res.reason}",
            recommended_actions=w_res.recommended_actions,
            safety_notes=[
                f"Current Temp: {w_res.temperature_celsius}°C, Humidity: {w_res.humidity_percent}%",
                "Monitor forecast before spraying chemical pesticides."
            ],
            escalation_flag=False
        )
        return ChatMessageResponse(
            intent="weather_risk",
            session_id=payload.session_id,
            advisory=translate_advisory(raw_advisory, lang),
            weather_risk=w_res.model_dump()
        )

    # INTENT 4: GENERAL / UNRELATED
    raw_advisory = AdvisoryResponse(
        diagnosis_or_answer="I can currently help with crop health, crop diseases, pests, weather risks and agricultural guidance.",
        recommended_actions=[
            "Scan a leaf photo for disease diagnosis.",
            "Ask questions like 'Meri fasal mein daag hain' or 'Rice blast kya hai'.",
            "Check current weather disease risk alerts."
        ],
        safety_notes=["AgriRakshak is specialized exclusively for agriculture and crop protection."],
        escalation_flag=False
    )
    return ChatMessageResponse(
        intent="general",
        session_id=payload.session_id,
        advisory=translate_advisory(raw_advisory, lang)
    )
