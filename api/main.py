# api/main.py
from fastapi import FastAPI
from core.config import settings
from routers import lead_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Core API for LeadFlow Real Estate Scoring and Orchestration"
)

# --- SECURITY: CORS CONFIGURATION ---
# Allows external frontend applications (like Lovable/React/Vite) to communicate with this API.
# In production, you should restrict allow_origins to your specific frontend domains.
# --- SECURITY: CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],    # Allows all origins for MVP development. Change to specific URLs later.
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],    # Allows all headers (Authorization, Content-Type, etc.)
)

# Register the router with a standard API prefix
app.include_router(lead_router.router, prefix="/api/v1/leads", tags=["Leads"])

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {"status": "healthy", "service": settings.PROJECT_NAME}