# api/routers/lead_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.lead_schema import WebhookPayload, LeadResponse
from core.database import get_db
from services import lead_service

# Initialize the router
router = APIRouter()

@router.post("/webhook", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def receive_whatsapp_lead(payload: WebhookPayload, db: Session = Depends(get_db)):
    """
    Endpoint to receive raw incoming messages from n8n.
    """
    try:
        lead = lead_service.process_incoming_webhook(db=db, payload=payload)

        return LeadResponse(
            lead_id=lead.id,
            status="success",
            message=f"Interaction securely logged.",
            assigned_score=lead.score.value # Return the enum value (e.g., 'hot', 'warm')
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")