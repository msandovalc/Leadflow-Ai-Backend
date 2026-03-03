from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .base import AuditableModel


class Tenant(AuditableModel):
    """
    Represents a client (Real Estate Agency / Inmobiliaria).
    """
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(100), index=True)
    whatsapp_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationship: One tenant can have many leads
    leads: Mapped[List["Lead"]] = relationship("Lead", back_populates="tenant", cascade="all, delete-orphan")