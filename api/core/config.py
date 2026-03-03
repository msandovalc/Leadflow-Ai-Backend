# api/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Master application settings.
    Pydantic will automatically read these variables from the .env file or OS environment.
    """
    PROJECT_NAME: str = "LeadFlow AI Backend"
    API_VERSION: str = "v1"

    # Default database URL (for local development purposes)
    # In production (Docker), this variable is overwritten by docker-compose environment variables
    # DATABASE_URL: str = "postgresql://user:password_seguro_db@localhost:5432/leadflow"
    DATABASE_URL: str = "postgresql://user:password_seguro_db@127.0.0.1:5433/leadflow"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate the settings object so other modules can import it directly
settings = Settings()