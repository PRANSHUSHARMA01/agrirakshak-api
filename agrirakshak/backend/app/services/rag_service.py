import os
import re
import requests
from typing import List, Dict, Any, Optional
from app.config import settings
from app.schemas.chat import AdvisoryResponse

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")

def search_local_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Scans local knowledge base markdown files and returns matching snippets based on keyword relevance.
    """
    query_words = set(re.findall(r'\w+', query.lower()))
    matches = []

    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Calculate keyword match score
                    score = sum(1 for word in query_words if word in content.lower() and len(word) > 2)
                    if score > 0:
                        matches.append({
                            "title": file.replace(".md", "").replace("_", " ").title(),
                            "content": content,
                            "score": score
                        })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

def query_gemini_api(system_prompt: str, user_query: str, api_key: str) -> Optional[str]:
    """
    Calls Google Gemini API using REST endpoint with fast 5-second timeout for interactive response.
    """
    if not api_key:
        return None

    full_prompt = f"{system_prompt}\n\nUSER MESSAGE: {user_query}"
    models = ["gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-flash-latest"]

    for model_name in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"maxOutputTokens": 450, "temperature": 0.4}
            }
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                candidates = resp.json().get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                        if text:
                            return text
        except Exception as e:
            print(f"Gemini API error ({model_name}): {e}")

    return None

def synthesize_dynamic_advisory(query: str, search_results: List[Dict[str, str]]) -> AdvisoryResponse:
    """
    Synthesizes a unique, interactive, question-specific response based on query intent and ICAR knowledge base.
    """
    q_lower = query.lower().strip()
    is_hindi = any("\u0900" <= char <= "\u097F" for char in query) or any(w in q_lower for w in ["daag", "fasal", "dhan", "kya", "ilaj", "rog", "karein", "namaste", "ram", "kaise"])

    # Greetings & General Conversational Intent
    if any(w in q_lower for w in ["hello", "hi", "hey", "namaste", "ram ram", "pranam", "who are you", "kaun ho", "kaise ho", "help"]):
        if is_hindi:
            answer = "राम-राम किसान भाई! मैं **AgriRakshak AI** हूँ, आपका व्यक्तिगत कृषि मित्र। आप मुझसे फसलों के रोग, कीड़े, खाद, सिंचाई, मौसम या फसल सुरक्षा से जुड़ा कोई भी सवाल पूछ सकते हैं।"
        else:
            answer = "Greetings farmer! I am **AgriRakshak AI**, your personal agricultural companion. You can ask me about crop diseases, pest control, fertilizers, irrigation, or weather alerts."
        
        return AdvisoryResponse(
            diagnosis_or_answer=answer,
            recommended_actions=[
                "Ask a question like 'Dhan me brown spot ka ilaj kya hai'.",
                "Scan or upload a photo of your crop leaf for instant diagnosis.",
                "Check current weather risk alerts for your district."
            ],
            safety_notes=["AgriRakshak is specialized for Indian farming & ICAR agronomy."],
            escalation_flag=False
        )

    if not search_results:
        if is_hindi:
            answer = f"राम-राम किसान भाई! **'{query}'** के बारे में: अपनी फसल की पत्तियों और तने का निरीक्षण करें। संतुलित उर्वरक (NPK) प्रयोग करें, सही जल निकासी रखें और आवश्यकता होने पर नजदीकी कृषि विज्ञान केंद्र (KVK) से सलाह लें।"
        else:
            answer = f"Greetings farmer! Regarding **'{query}'**: Monitor your crop daily for early symptoms, maintain proper field drainage, apply balanced NPK fertilizers, and consult your local extension officer."
        
        return AdvisoryResponse(
            diagnosis_or_answer=answer,
            recommended_actions=[
                "Inspect leaves daily for early spots, yellowing, or wilting.",
                "Ensure proper field drainage and avoid standing water.",
                "Consult local Krishi Vigyan Kendra (KVK) for specialized advice."
            ],
            safety_notes=["Follow official label directions for all spray applications."],
            escalation_flag=False
        )

    top_doc = search_results[0]
    title = top_doc['title']
    content = top_doc['content']
    lines = content.split("\n")

    # Extract relevant sections based on user query intent
    overview_text = ""
    symptoms = []
    actions = []
    safety = []

    current_section = None
    for line in lines:
        l_str = line.strip()
        if line.startswith("## Overview") or line.startswith("## Identification"):
            current_section = "overview"
        elif line.startswith("## Symptoms"):
            current_section = "symptoms"
        elif any(line.startswith(h) for h in ["## Prevention", "## Control", "## Chemical Control", "## Cultural Control"]):
            current_section = "control"
        elif line.startswith("## Safety"):
            current_section = "safety"
        elif line.startswith("## "):
            current_section = None
        else:
            if current_section == "overview" and l_str and not l_str.startswith("#"):
                overview_text += " " + l_str
            elif current_section == "symptoms" and l_str.startswith("- "):
                symptoms.append(l_str.lstrip("- ").strip())
            elif current_section == "control" and l_str.startswith("- "):
                actions.append(l_str.lstrip("- ").strip())
            elif current_section == "safety" and l_str.startswith("- "):
                safety.append(l_str.lstrip("- ").strip())

    # Customize answer based on query
    if any(w in q_lower for w in ["symptom", "identify", "pechan", "daag", "spot", "look"]):
        if symptoms:
            answer = f"Based on **AgriRakshak Knowledge Base ({title}) Symptoms**:\n\n" + " ".join(symptoms[:3])
        else:
            answer = f"Based on **AgriRakshak Knowledge Base ({title})**:\n\n{overview_text[:280]}..."
    elif any(w in q_lower for w in ["treat", "control", "spray", "ilaj", "dawai", "remedy", "cure"]):
        answer = f"Based on **AgriRakshak Knowledge Base ({title}) Recommended Treatments**:\n\n{overview_text[:250]}..."
    else:
        answer = f"Based on **AgriRakshak Knowledge Base ({title})**:\n\n{overview_text[:300]}..."

    if is_hindi:
        answer = f"राम-राम किसान भाई! **{title}** के संदर्भ में:\n\n" + (overview_text[:280] if overview_text else "अपनी फसल की नियमित जांच करें।")

    if not actions:
        actions = symptoms[:3] if symptoms else [
            "Inspect affected crop leaves daily for spreading spots.",
            "Maintain proper field drainage and balanced fertilization.",
            "Remove diseased leaves to prevent spore transmission."
        ]
    if not safety:
        safety = [
            "Always follow official product labels and recommended spray dosages.",
            "Wear protective gloves and mask when applying agricultural sprays.",
            "Consult local Krishi Vigyan Kendra (KVK) for regional advice."
        ]

    return AdvisoryResponse(
        diagnosis_or_answer=answer.strip(),
        recommended_actions=actions[:4],
        safety_notes=safety[:3],
        escalation_flag=False
    )

def query_rag(query: str, crop: Optional[str] = None) -> AdvisoryResponse:
    """
    Queries AgriRakshak AI RAG pipeline to answer agricultural questions.
    """
    search_results = search_local_knowledge_base(query)

    # 1. Try Gemini API if API key provided
    gemini_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        context_text = "\n\n".join([r["content"] for r in search_results[:2]])
        system_prompt = (
            "You are AgriRakshak, a helpful, conversational AI agricultural assistant for Indian farmers. "
            "Reply warmly and interactively. Answer the user's exact message directly. "
            "If in Hindi, reply in friendly Hindi. If in English, reply in clear English."
        )
        if context_text:
            system_prompt += f"\nICAR CONTEXT:\n{context_text}"
        
        ai_output = query_gemini_api(system_prompt, query, gemini_key)
        if ai_output:
            return AdvisoryResponse(
                diagnosis_or_answer=ai_output,
                recommended_actions=["Inspect crops daily for symptoms.", "Maintain field drainage.", "Follow label instructions."],
                safety_notes=["Consult local extension officers for regional advice."],
                escalation_flag=False
            )

    # 2. Dynamic interactive Q&A synthesis tailored to user query
    return synthesize_dynamic_advisory(query, search_results)
