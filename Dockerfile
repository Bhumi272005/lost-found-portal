# Railway FastAPI Backend Deployment
# This builds ONLY the FastAPI backend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Verify FastAPI can be imported
RUN python -c "from backend.main import app; print('✅ FastAPI backend ready for deployment')"

# Expose port (Railway will set $PORT)
EXPOSE 8000

# Start FastAPI with proper environment variable handling
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info
