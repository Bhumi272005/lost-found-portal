# Railway FastAPI Backend Deployment
# This builds ONLY the FastAPI backend (excludes Streamlit)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy backend-only requirements and install
COPY requirements-backend.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY backend files (not frontend)
COPY backend/ ./backend/
COPY check_image_urls.py ./
COPY mongod.conf ./

# Verify FastAPI is accessible by creating a simple test
RUN python -c "from backend.main import app; print('✅ FastAPI app imported successfully')"

# Start FastAPI backend on Railway's port
CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT --log-level info
