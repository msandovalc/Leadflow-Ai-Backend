# api/schemas/lead_schema.py
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class WebhookPayload(BaseModel):
    """
    Pydantic schema to validate incoming webhook data from n8n / Evolution API.
    Ensures all required data for legal tracking is present.
    """
    tenant_id: uuid.UUID = Field(..., description="The unique ID of the Real Estate Agency")
    whatsapp_number: str = Field(..., min_length=10, description="The prospect's phone number")
    message_content: str = Field(..., description="The actual message received from the prospect")

    # Optional metadata that n8n might send (like agent ID, property ID, etc.)
    metadata_payload: dict | None = Field(default=None, description="Optional flexible data")


class LeadResponse(BaseModel):
    """
    Standard response schema including the AI evaluation results.
    """
    lead_id: uuid.UUID
    status: str
    message: str
    assigned_score: str | None = None # Added to return the score to n8n


class InteractionResponse(BaseModel):
    """
    Schema representing a single interaction (message or AI evaluation)
    associated with a lead.
    """
    id: uuid.UUID
    interaction_type: str
    content: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True # Enables reading from SQLAlchemy models


class LeadDetailResponse(BaseModel):
    """
    Comprehensive schema for a Lead, including its interactions.
    Used by the Frontend (Lovable) to display lead details.
    """
    id: uuid.UUID
    whatsapp_number: str
    score: str | None = None
    intent: str | None = None
    budget: str | None = None
    preferred_zone: str | None = None
    created_at: datetime | None = None
    interactions: list[InteractionResponse] = []

    class Config:
        from_attributes = True


class DashboardMetricsResponse(BaseModel):
    """
    Schema for the high-level metrics displayed on the main dashboard.
    """
    total_leads: int
    hot_leads: int
    warm_leads: int
    cold_leads: int
    unrated_leads: int