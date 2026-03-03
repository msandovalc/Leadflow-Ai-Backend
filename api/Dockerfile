FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install system dependencies required for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy ONLY the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
# --no-interaction: Do not ask any interactive question
# --no-ansi: Disable ANSI output
# --no-root: Do not install the current project package itself
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . /app/

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]