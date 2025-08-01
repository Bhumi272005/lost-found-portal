# Railway FastAPI Backend Deployment
# This builds the BACKEND only (not Streamlit frontend)
FROM python:3.11-slim

WORKDIR /app

# Install curl for potential debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/
COPY *.py ./

# Start FastAPI backend
CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT
