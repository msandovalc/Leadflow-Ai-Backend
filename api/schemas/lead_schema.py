# api/schemas/lead_schema.py
from pydantic import BaseModel, Field
import uuid


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