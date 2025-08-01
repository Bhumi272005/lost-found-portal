# Railway-optimized Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Railway will set the PORT environment variable
EXPOSE $PORT

# Start the application
CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT
