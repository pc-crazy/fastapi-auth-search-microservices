# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.6.1

# Set working directory
WORKDIR /app

# Copy all source code
COPY . .

# Install dependencies for auth and search services
RUN pip install --no-cache-dir -r services/auth_service/requirements.txt && \
    pip install --no-cache-dir -r services/search_service/requirements.txt

# Set environment (make sure .env exists in the project root)
ENV AUTH_SERVICE_DATABASE_URL=sqlite:///./service/auth/auth.db
ENV SEARCH_SERVICE_DATABASE_URL=sqlite:///./service/search/search.db

# Initialize databases and seed data
RUN python -m services.auth_service.init_db && \
    python -m services.search_service.init_db && \
    python -m services.search_service.seed_faker_employees

# Expose both services
EXPOSE 8000 8001

# Default command placeholder (will be overridden by docker-compose)
CMD ["uvicorn", "services.search_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
