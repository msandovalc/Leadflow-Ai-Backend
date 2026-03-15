# api/services/lead_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid
import logging
from models.lead import Lead, LeadScore
from models.interaction import Interaction
from schemas.lead_schema import WebhookPayload
from services import scoring_service

# Initialize logger for service layer
logger = logging.getLogger(__name__)


def process_incoming_webhook(db: Session, payload: WebhookPayload) -> Lead:
    """
    Core business logic to handle an incoming WhatsApp message.
    Includes AI intent analysis and lead scoring.
    """
    # Check if lead already exists for this agency
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
        db.flush()  # Get ID without committing

    # 1. AI Analysis: Evaluate intent and budget
    try:
        analysis = scoring_service.evaluate_lead_intent(payload.message_content)

        # 2. Update Lead profile with AI insights
        lead.intent = analysis.get("intent")
        lead.budget = analysis.get("budget")
        lead.preferred_zone = analysis.get("preferred_zone")
        lead.score = analysis.get("score", LeadScore.UNRATED)
    except Exception as e:
        logger.warning(f"AI Scoring failed, falling back to defaults: {str(e)}")

    # 3. Log the incoming message
    interaction = Interaction(
        lead_id=lead.id,
        interaction_type="wa_message_in",
        content=payload.message_content
    )
    db.add(interaction)

    # 4. Log AI evaluation for traceability
    ai_interaction = Interaction(
        lead_id=lead.id,
        interaction_type="ai_evaluation",
        content=f"AI System: Analysis complete. Result: {lead.score}"
    )
    db.add(ai_interaction)

    db.commit()
    db.refresh(lead)
    return lead


def get_leads_by_tenant(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of leads for the dashboard grid.
    """
    return db.query(Lead).filter(Lead.tenant_id == tenant_id) \
        .order_by(Lead.created_at.desc()) \
        .offset(skip).limit(limit).all()


def get_lead_details(db: Session, lead_id: uuid.UUID, tenant_id: uuid.UUID):
    """
    Retrieves a single lead and manually fetches interaction history.
    """
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.tenant_id == tenant_id
    ).first()

    if not lead:
        return None

    interactions = db.query(Interaction).filter(Interaction.lead_id == lead.id) \
        .order_by(Interaction.created_at.asc()).all()

    lead.interactions = interactions
    return lead


def get_tenant_metrics(db: Session, tenant_id: uuid.UUID) -> dict:
    """
    Calculates KPIs for the frontend dashboard.
    Fix: Ensures Enum values are converted to strings for correct mapping.
    """
    try:
        total = db.query(Lead).filter(Lead.tenant_id == tenant_id).count()

        # Aggregation query for scores
        score_counts = db.query(Lead.score, func.count(Lead.id)) \
            .filter(Lead.tenant_id == tenant_id) \
            .group_by(Lead.score).all()

        # FIX: Explicitly convert Enum objects to their string values (e.g., 'hot', 'warm')
        # This prevents the 500 error during dictionary lookup
        counts_dict = {}
        for score_enum, count in score_counts:
            key = score_enum.value if hasattr(score_enum, 'value') else str(score_enum)
            counts_dict[key] = count

        return {
            "total_leads": total,
            "hot_leads": counts_dict.get("hot", 0),
            "warm_leads": counts_dict.get("warm", 0),
            "cold_leads": counts_dict.get("cold", 0),
            "unrated_leads": counts_dict.get("unrated", 0)
        }
    except Exception as e:
        logger.error(f"Metrics calculation error: {str(e)}")
        raise e