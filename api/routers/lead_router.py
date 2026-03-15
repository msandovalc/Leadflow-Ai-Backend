# api/routers/lead_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.lead_schema import WebhookPayload, LeadResponse, LeadDetailResponse, DashboardMetricsResponse
from core.database import get_db
from services import lead_service
import uuid
import logging
from typing import List

# Setup logger to capture backend crashes in Docker logs
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/webhook", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def receive_whatsapp_lead(payload: WebhookPayload, db: Session = Depends(get_db)):
    """
    Endpoint to receive incoming lead data from the n8n automation pipeline.
    """
    try:
        lead = lead_service.process_incoming_webhook(db=db, payload=payload)
        return LeadResponse(
            lead_id=lead.id,
            status="success",
            message="Interaction securely logged.",
            assigned_score=lead.score.value
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during webhook processing")

@router.get("/metrics", response_model=DashboardMetricsResponse)
def get_dashboard_metrics(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Fetches KPI metrics for the frontend dashboard.
    Note: This is the likely source of the 500 error due to potential empty dataset calculations.
    """
    try:
        metrics = lead_service.get_tenant_metrics(db=db, tenant_id=tenant_id)
        return metrics
    except Exception as e:
        logger.error(f"Failed to fetch metrics for tenant {tenant_id}: {str(e)}")
        # We return the specific error string to debug it in the browser's Network tab
        raise HTTPException(status_code=500, detail=f"Database/Service error: {str(e)}")

@router.get("", response_model=List[LeadDetailResponse])
def get_all_leads(tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lists all leads associated with a specific real estate agency (tenant).
    Path changed from '/' to '' to prevent 307 Temporary Redirects.
    """
    try:
        leads = lead_service.get_leads_by_tenant(db=db, tenant_id=tenant_id, skip=skip, limit=limit)
        return leads
    except Exception as e:
        logger.error(f"Error retrieving leads list: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve leads")

@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_single_lead(lead_id: uuid.UUID, tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Retrieves full profile and interaction history for a specific lead.
    """
    try:
        lead = lead_service.get_lead_details(db=db, lead_id=lead_id, tenant_id=tenant_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found or access denied")
        return lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lead detail for {lead_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")