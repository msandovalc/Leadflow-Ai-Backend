import enum
import uuid
from sqlalchemy import String, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import AuditableModel


class LeadScore(str, enum.Enum):
    """Enumeration for standardized ML/AI scoring."""
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    UNRATED = "unrated"


class Lead(AuditableModel):
    """
    Represents a potential buyer/renter that contacted via WhatsApp.
    """
    __tablename__ = "leads"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)

    # Contact Info
    whatsapp_number: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str | None] = mapped_column(String(100))

    # AI Extracted Qualifications
    intent: Mapped[str | None] = mapped_column(String(50))  # e.g., 'buy', 'rent'
    budget: Mapped[str | None] = mapped_column(String(100))
    preferred_zone: Mapped[str | None] = mapped_column(String(150))

    # Scoring
    score: Mapped[LeadScore] = mapped_column(Enum(LeadScore), default=LeadScore.UNRATED, index=True)

    # JSON field for flexible raw data from n8n/Evolution API
    metadata_payload: Mapped[dict | None] = mapped_column(JSON)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="leads")
    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="lead",
                                                             cascade="all, delete-orphan")