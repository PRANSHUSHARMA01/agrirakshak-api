from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database import get_db
from app.services.prediction_client import prediction_client
from app.models.farmer_case import FarmerCase
from app.schemas.prediction import PredictionResponse

router = APIRouter(prefix="/prediction", tags=["Prediction"])

@router.post("/analyze", response_model=PredictionResponse)
async def analyze_crop_image(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form("demo-session"),
    crop: Optional[str] = Form("Rice"),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Direct endpoint to analyze uploaded crop image via prediction microservice.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file format.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds maximum 10MB limit.")

    result = prediction_client.predict_image(contents, filename=file.filename or "leaf.jpg")

    # Persist case in database
    farmer_case = FarmerCase(
        session_id=session_id,
        image_url=file.filename,
        crop=crop,
        predicted_class=result.get("predicted_class"),
        confidence=result.get("confidence", 0.0),
        latitude=latitude,
        longitude=longitude,
        status="diagnosed" if result.get("success") else "failed",
        needs_expert_review=result.get("needs_expert_review", False),
        raw_prediction=json.dumps(result.get("raw_response", {}))
    )
    db.add(farmer_case)
    db.commit()
    db.refresh(farmer_case)

    return result
