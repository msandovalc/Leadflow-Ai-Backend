import uuid
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import AuditableModel


class Interaction(AuditableModel):
    """
    Immutable log of interactions (WhatsApp messages, system notes, AI evaluations).
    Acts as irrefutable proof of lead attribution.
    """
    __tablename__ = "interactions"

    lead_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), index=True)

    interaction_type: Mapped[str] = mapped_column(
        String(50))  # e.g., 'wa_message_in', 'wa_message_out', 'ai_score_update'
    content: Mapped[str] = mapped_column(Text)  # The actual message or system note

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="interactions")