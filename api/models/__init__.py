# api/models/__init__.py
from .base import Base, AuditableModel
from .tenant import Tenant
from .lead import Lead, LeadScore
from .interaction import Interaction

# By exporting them here, Alembic (migration tool) can detect all metadata
# just by importing Base from api.models