# api/routers/lead_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.lead_schema import WebhookPayload, LeadResponse
from core.database import get_db
from services import lead_service
import uuid
from typing import List
from schemas.lead_schema import LeadDetailResponse, DashboardMetricsResponse

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


@router.get("/metrics", response_model=DashboardMetricsResponse)
def get_dashboard_metrics(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Endpoint to fetch KPIs for the frontend dashboard.
    Requires tenant_id as a query parameter (Multi-tenant design).
    """
    try:
        metrics = lead_service.get_tenant_metrics(db=db, tenant_id=tenant_id)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/", response_model=List[LeadDetailResponse])
def get_all_leads(tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to list all leads for a specific real estate agency.
    """
    try:
        leads = lead_service.get_leads_by_tenant(db=db, tenant_id=tenant_id, skip=skip, limit=limit)
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_single_lead(lead_id: uuid.UUID, tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the full context and chat history of a specific lead.
    """
    try:
        lead = lead_service.get_lead_details(db=db, lead_id=lead_id, tenant_id=tenant_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found or unauthorized")
        return lead
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")