# Railway FastAPI Backend Deployment
# This builds ONLY the FastAPI backend (excludes Streamlit)
FROM python:3.11-slim

# Set environment variables with defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV LOG_LEVEL=info
ENV WORKERS=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY backend files (not frontend)
COPY backend/ ./backend/

# Verify FastAPI is accessible by creating a simple test
RUN python -c "from backend.main import app; print('✅ FastAPI app imported successfully')"

# Expose the port (Railway will override with $PORT)
EXPOSE $PORT

# Start FastAPI backend using environment variables
CMD uvicorn backend.main:app --host $HOST --port $PORT --log-level $LOG_LEVEL --workers $WORKERS
