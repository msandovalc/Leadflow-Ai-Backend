# api/services/lead_service.py
from sqlalchemy.orm import Session
from models.lead import Lead, LeadScore
from models.interaction import Interaction
from schemas.lead_schema import WebhookPayload
from services import scoring_service  # Import the new AI service


def process_incoming_webhook(db: Session, payload: WebhookPayload) -> Lead:
    """
    Core business logic to handle an incoming WhatsApp message from n8n.
    Now includes AI scoring integration.
    """
    lead = db.query(Lead).filter(
        Lead.tenant_id == payload.tenant_id,
        Lead.whatsapp_number == payload.whatsapp_number
    ).first()

    if not lead:
        lead = Lead(
            tenant_id=payload.tenant_id,
            whatsapp_number=payload.whatsapp_number,
            score=LeadScore.UNRATED,
            metadata_payload=payload.metadata_payload
        )
        db.add(lead)
        db.flush()

        # 1. Evaluate the lead using the AI Scoring Service
    analysis = scoring_service.evaluate_lead_intent(payload.message_content)

    # 2. Update the lead with the AI extracted data
    lead.intent = analysis["intent"]
    lead.budget = analysis["budget"]
    lead.preferred_zone = analysis["preferred_zone"]
    lead.score = analysis["score"]

    # 3. Create the immutable interaction log
    interaction = Interaction(
        lead_id=lead.id,
        interaction_type="wa_message_in",
        content=payload.message_content
    )
    db.add(interaction)

    # 4. Optional: Log the AI evaluation as a system interaction for full traceability
    ai_interaction = Interaction(
        lead_id=lead.id,
        interaction_type="ai_evaluation",
        content=f"Scored as {analysis['score']} - Intent: {analysis['intent']}"
    )
    db.add(ai_interaction)

    db.commit()
    db.refresh(lead)

    return lead