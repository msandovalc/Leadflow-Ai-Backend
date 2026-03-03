# api/services/scoring_service.py
from models.lead import LeadScore


def evaluate_lead_intent(message_content: str) -> dict:
    """
    Simulates an LLM (Claude/GPT) call to analyze the lead's message.
    Extracts the user intent, budget, preferred zone, and assigns a score.

    TODO: Replace the mock logic below with an actual call to the OpenAI/Anthropic API
    using a structured JSON output prompt.
    """

    # We convert to lowercase for the mock evaluation
    message_lower = message_content.lower()

    # Default values
    score = LeadScore.UNRATED
    intent = "unknown"
    budget = "unknown"
    preferred_zone = "unknown"

    # Mock NLP Logic (To be replaced by real AI)
    if "comprar" in message_lower or "compra" in message_lower:
        intent = "buy"
        score = LeadScore.HOT if "millones" in message_lower else LeadScore.WARM
    elif "rentar" in message_lower or "renta" in message_lower:
        intent = "rent"
        score = LeadScore.WARM

    if "presupuesto" in message_lower or "millones" in message_lower:
        # Extremely basic mock extraction
        budget = "2 millones" if "2" in message_lower else "specified"

    if "zona sur" in message_lower:
        preferred_zone = "zona sur"
    elif "centro" in message_lower:
        preferred_zone = "centro"

    return {
        "intent": intent,
        "budget": budget,
        "preferred_zone": preferred_zone,
        "score": score
    }