from typing import List, Dict
from app.schemas.chat import AdvisoryResponse

# Dictionary for common agricultural advisories in Hindi
HINDI_TRANSLATION_MAP: Dict[str, str] = {
    "Detected Rice Blast with": "चावल में राइस ब्लास्ट (Rice Blast) रोग की पहचान हुई है। विश्वसनीयता:",
    "Detected Bacterial Leaf Blight with": "चावल में बैक्टीरियल लीफ ब्लाइट (Bacterial Leaf Blight) के लक्षण मिले हैं। विश्वसनीयता:",
    "Detected Rice Skipper (Pest) with": "चावल की फसल में राइस स्किपर कीट (Rice Skipper) का प्रकोप पाया गया है। विश्वसनीयता:",
    "Detected White Stem Borer (Rice Pest) with": "चावल की फसल में तना छेदक कीट (White Stem Borer) का प्रभाव दिखा है। विश्वसनीयता:",
    "Detected Brown Spot (Rice Fungal Disease) with": "चावल की पत्तियों पर भूरे धब्बों (Brown Spot) की पहचान हुई है। विश्वसनीयता:",
    
    # Common actions in Hindi
    "Remove severely infected leaves and discard outside the field.": "संक्रमित पत्तियों को खेत से हटाकर नष्ट करें।",
    "Maintain optimal field drainage; avoid prolonged waterlogging.": "खेत में जल निकासी की उचित व्यवस्था रखें; लंबे समय तक पानी न भरने दें।",
    "Avoid excessive application of nitrogenous fertilizers.": "आवश्यकता से अधिक यूरिया (नाइट्रोजन) का प्रयोग न करें।",
    "Ensure proper spacing between plants for good aeration.": "पौधों के बीच उचित दूरी बनाएं ताकि हवा का आवागमन बना रहे।",
    "Manually collect and destroy larvae and folded leaf webs in early stages.": "शुरुआती चरण में सुंडी और पत्ती के जालों को इकट्ठा करके नष्ट करें।",
    "Maintain clean field borders and remove weed hosts.": "मेड़ों को साफ रखें और खरपतवार नष्ट करें।",
    "Encourage natural predators like parasitoid wasps and spiders.": "मित्र कीटों जैसे मकड़ियों और परजीवियों को संरक्षित करें।",
    "Clip leaf tips before transplanting to remove egg masses.": "रोपाई से पहले पौध की ऊपरी पत्तियों की कटाई करें ताकि कीट के अंडे हट जाएं।",
    "Set up light traps or pheromone traps to monitor adult moth activity.": "वयस्क कीटों की निगरानी के लिए लाइट ट्रैप या फेरोमोन ट्रैप लगाएं।",
    "Submerge stubbles after harvest to destroy overwintering larvae.": "कटाई के बाद ठूंठों को पानी में डुबोएं ताकि बचे हुए कीड़े नष्ट हो जाएं।",
    "Use disease-free certified seeds.": "रोगमुक्त और प्रमाणित बीजों का ही उपयोग करें।",
    "Apply balanced fertilizer containing Potassium and Micronutrients.": "पोटाश और सूक्ष्म पोषक तत्वों का संतुलित प्रयोग करें।",
    "Avoid drought stress during critical growth stages.": "फसल की वृद्धि के दौरान सूखे का तनाव न आने दें।",
    
    # Safety notes in Hindi
    "Follow locally approved agricultural recommendations.": "स्थानीय कृषि अधिकारियों की संस्तुति का पालन करें।",
    "Do not apply chemicals without checking the official label and recommended dosage.": "कीटनाशक का प्रयोग बिना लेबल और सही मात्रा जांचे न करें।",
    "Consult your nearest Krishi Vigyan Kendra (KVK) for regional advisories.": "अधिक जानकारी के लिए नजदीकी कृषि विज्ञान केंद्र (KVK) से संपर्क करें।",
    "Avoid broad-spectrum chemical sprays that kill beneficial insects.": "घातक रसायनों का अनावश्यक छिड़काव न करें जिससे मित्र कीट मरते हैं।",
    "Always follow safety precautions and wear protective equipment when spraying.": "छिड़काव करते समय दस्ताने और मास्क पहनकर सुरक्षा बरतें।"
}

def translate_text_to_hindi(text: str) -> str:
    """
    Translates English agricultural text to Hindi using dictionary map or pattern replacement.
    """
    for eng, hin in HINDI_TRANSLATION_MAP.items():
        if eng in text:
            text = text.replace(eng, hin)

    # Basic pattern replacements
    text = text.replace("confidence", "विश्वसनीयता")
    text = text.replace("Low confidence detection: escalated for agricultural expert review", "कम विश्वसनीयता के कारण विशेषज्ञ समीक्षा हेतु भेजा गया है")
    text = text.replace("Weather Risk Assessment", "मौसम जोखिम मूल्यांकन")
    text = text.replace("Level HIGH", "स्तर: उच्च (HIGH)")
    text = text.replace("Level MEDIUM", "स्तर: मध्यम (MEDIUM)")
    text = text.replace("Level LOW", "स्तर: सामान्य (LOW)")
    text = text.replace("I'm not sure about that. Please consult your local Krishi Vigyan Kendra or agricultural extension officer.", "मुझे इसके बारे में निश्चित जानकारी नहीं है। कृपया अपने नजदीकी कृषि विज्ञान केंद्र या ब्लॉक कृषि अधिकारी से परामर्श लें।")

    return text

def translate_advisory(advisory: AdvisoryResponse, target_language: str = "en") -> AdvisoryResponse:
    """
    Translates structured advisory response to target language (en or hi).
    """
    if target_language.lower() != "hi":
        return advisory  # Default English

    translated_diag = translate_text_to_hindi(advisory.diagnosis_or_answer)
    translated_actions = [translate_text_to_hindi(a) for a in advisory.recommended_actions]
    translated_safety = [translate_text_to_hindi(s) for s in advisory.safety_notes]

    return AdvisoryResponse(
        diagnosis_or_answer=translated_diag,
        recommended_actions=translated_actions,
        safety_notes=translated_safety,
        escalation_flag=advisory.escalation_flag
    )
