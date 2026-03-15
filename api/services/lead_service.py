# api/services/lead_service.py
from sqlalchemy.orm import Session
from models.lead import Lead, LeadScore
from models.interaction import Interaction
from schemas.lead_schema import WebhookPayload
from services import scoring_service  # Import the new AI service
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid


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


def get_leads_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100):
    """
    Retrieves a paginated list of leads for a specific tenant.
    Used by the Lovable frontend data grid.
    """
    return db.query(Lead).filter(Lead.tenant_id == tenant_id) \
        .order_by(Lead.created_at.desc()) \
        .offset(skip).limit(limit).all()


def get_lead_details(db: Session, lead_id: uuid.UUID, tenant_id: uuid.UUID):
    """
    Retrieves a specific lead and its complete interaction history.
    Ensures the lead belongs to the requested tenant for security.
    """
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.tenant_id == tenant_id
    ).first()

    if not lead:
        return None

    # Manually fetch interactions if SQLAlchemy relationships (back_populates) are not fully configured
    interactions = db.query(Interaction).filter(Interaction.lead_id == lead.id) \
        .order_by(Interaction.created_at.asc()).all()

    # Attach interactions to the lead object dynamically for Pydantic serialization
    lead.interactions = interactions
    return lead


def get_tenant_metrics(db: Session, tenant_id: uuid.UUID) -> dict:
    """
    Calculates key performance indicators for the dashboard.
    Uses SQL aggregation for maximum performance instead of Python loops.
    """
    total = db.query(Lead).filter(Lead.tenant_id == tenant_id).count()

    # Query to count leads grouped by their score
    score_counts = db.query(Lead.score, func.count(Lead.id)) \
        .filter(Lead.tenant_id == tenant_id) \
        .group_by(Lead.score).all()

    # Convert list of tuples to a dictionary
    counts_dict = {score.value if hasattr(score, 'value') else score: count for score, count in score_counts}

    return {
        "total_leads": total,
        "hot_leads": counts_dict.get("hot", 0),
        "warm_leads": counts_dict.get("warm", 0),
        "cold_leads": counts_dict.get("cold", 0),
        "unrated_leads": counts_dict.get("unrated", 0)
    }