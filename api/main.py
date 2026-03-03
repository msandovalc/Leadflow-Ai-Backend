# api/main.py
from fastapi import FastAPI
from core.config import settings
from routers import lead_router # Import the newly created router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Core API for LeadFlow Real Estate Scoring and Orchestration"
)

# Register the router with a standard API prefix
app.include_router(lead_router.router, prefix="/api/v1/leads", tags=["Leads"])

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {"status": "healthy", "service": settings.PROJECT_NAME}