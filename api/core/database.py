# api/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create the SQLAlchemy engine (the core interface to the PostgreSQL database)
engine = create_engine(settings.DATABASE_URL, echo=False)

# Create a session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency Injection function for FastAPI endpoints.
    Opens a new database session per request and ensures it is closed when finished,
    preventing connection and memory leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()