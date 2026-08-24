from typing import Dict, Any, List
from app.schemas.chat import AdvisoryResponse

# Curated disease knowledge dictionary for standard predictions
DISEASE_ADVISORY_MAP: Dict[str, Dict[str, Any]] = {
    "01_Bacterial_leaf_blight": {
        "title": "Bacterial Leaf Blight (Rice)",
        "actions": [
            "Remove severely infected leaves and discard outside the field.",
            "Maintain optimal field drainage; avoid prolonged waterlogging.",
            "Avoid excessive application of nitrogenous fertilizers.",
            "Ensure proper spacing between plants for good aeration."
        ],
        "safety": [
            "Follow locally approved agricultural recommendations.",
            "Do not apply chemicals without checking the official label and recommended dosage.",
            "Consult your nearest Krishi Vigyan Kendra (KVK) for regional advisories."
        ]
    },
    "06_Rice_skipper": {
        "title": "Rice Skipper (Pest)",
        "actions": [
            "Manually collect and destroy larvae and folded leaf webs in early stages.",
            "Maintain clean field borders and remove weed hosts.",
            "Encourage natural predators like parasitoid wasps and spiders."
        ],
        "safety": [
            "Avoid broad-spectrum chemical sprays that kill beneficial insects.",
            "Always follow safety precautions and wear protective equipment when spraying."
        ]
    },
    "07_White_stem_borer": {
        "title": "White Stem Borer (Rice Pest)",
        "actions": [
            "Clip leaf tips before transplanting to remove egg masses.",
            "Set up light traps or pheromone traps to monitor adult moth activity.",
            "Submerge stubbles after harvest to destroy overwintering larvae."
        ],
        "safety": [
            "Use recommended bio-pesticides or approved insecticides at threshold levels only.",
            "Check local extension office guidelines for spray timings."
        ]
    },
    "Brown_Spot": {
        "title": "Brown Spot (Rice Fungal Disease)",
        "actions": [
            "Use disease-free certified seeds.",
            "Apply balanced fertilizer containing Potassium and Micronutrients.",
            "Avoid drought stress during critical growth stages."
        ],
        "safety": [
            "Do not exceed recommended chemical application rates.",
            "Ensure safe disposal of chemical containers after use."
        ]
    }
}

def generate_advisory(predicted_class: str, confidence: float, needs_expert_review: bool) -> AdvisoryResponse:
    """
    Constructs a structured advisory response from prediction result.
    """
    clean_name = predicted_class.replace("_", " ")
    
    # Match against advisory map or generate safe generic response
    info = DISEASE_ADVISORY_MAP.get(predicted_class)
    if not info:
        # Generic match based on key words
        if "blight" in predicted_class.lower():
            title = f"Leaf Blight ({clean_name})"
            actions = [
                "Remove and burn infected crop leaves.",
                "Ensure proper drainage and avoid leaf wetness over night.",
                "Balance soil nutrients to boost plant resistance."
            ]
        elif "spot" in predicted_class.lower():
            title = f"Fungal Leaf Spot ({clean_name})"
            actions = [
                "Remove affected leaves to slow down fungal spore spreading.",
                "Avoid overhead irrigation during humid weather.",
                "Maintain clean weed-free borders around the field."
            ]
        elif "borer" in predicted_class.lower() or "skipper" in predicted_class.lower() or "pest" in predicted_class.lower():
            title = f"Insect Pest Infestation ({clean_name})"
            actions = [
                "Install pest traps and monitor crop damage daily.",
                "Clear alternate weed hosts around the farm.",
                "Promote natural predator populations."
            ]
        else:
            title = f"Crop Condition: {clean_name}"
            actions = [
                "Inspect nearby plants for similar symptoms.",
                "Ensure proper field drainage and balanced fertilization.",
                "Keep leaves dry and monitor progression for 48 hours."
            ]
        
        safety = [
            "Follow locally approved agricultural recommendations.",
            "Do not apply pesticides without checking the recommended label/dose.",
            "Contact your local Krishi Vigyan Kendra for specialized guidance."
        ]
    else:
        title = info["title"]
        actions = info["actions"]
        safety = info["safety"]

    conf_pct = int(round(confidence * 100))
    if needs_expert_review:
        diagnosis = f"Detected possible {title} with {conf_pct}% confidence. (Low confidence detection: escalated for agricultural expert review)."
    else:
        diagnosis = f"Detected {title} with {conf_pct}% confidence."

    return AdvisoryResponse(
        diagnosis_or_answer=diagnosis,
        recommended_actions=actions,
        safety_notes=safety,
        escalation_flag=needs_expert_review
    )
