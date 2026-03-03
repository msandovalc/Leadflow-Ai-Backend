# api/seed_tenant.py
from core.database import SessionLocal
from models.tenant import Tenant
import uuid

def seed_first_tenant():
    """
    Creates the first Real Estate Agency (Tenant) in the database
    to satisfy the Foreign Key constraints when creating leads.
    """
    db = SessionLocal()
    try:
        # Check if we already have a tenant to avoid duplicates
        existing_tenant = db.query(Tenant).first()
        if existing_tenant:
            print(f"✅ Tenant already exists! Use this UUID: {existing_tenant.id}")
            return

        # Create a new demo tenant
        new_tenant = Tenant(
            name="Inmobiliaria Demo 2026",
            whatsapp_number="5213300000000"
        )
        db.add(new_tenant)
        db.commit()
        db.refresh(new_tenant)
        print(f"🚀 Success! New Tenant created.")
        print(f"👉 COPY THIS UUID FOR YOUR TEST: {new_tenant.id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_first_tenant()