# Railway Streamlit Frontend Deployment
# This builds the Streamlit frontend
FROM python:3.11-slim

# Set environment variables with defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8501
ENV HOST=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit frontend files
COPY frontend-streamlit/ ./
COPY .streamlit/ ./.streamlit/

# Verify Streamlit is accessible
RUN python -c "import streamlit; print('✅ Streamlit imported successfully')"

# Create a Python startup script to handle environment variables properly
RUN echo 'import os\n\
import subprocess\n\
import sys\n\
\n\
def main():\n\
    port = os.getenv("PORT", "8501")\n\
    host = os.getenv("HOST", "0.0.0.0")\n\
    \n\
    print(f"🚀 Starting Streamlit on {host}:{port}")\n\
    \n\
    cmd = [\n\
        "streamlit", "run", "streamlit_app.py",\n\
        "--server.port", str(port),\n\
        "--server.address", host,\n\
        "--server.headless", "true",\n\
        "--server.enableCORS", "false",\n\
        "--server.enableXsrfProtection", "false"\n\
    ]\n\
    \n\
    try:\n\
        subprocess.run(cmd, check=True)\n\
    except subprocess.CalledProcessError as e:\n\
        print(f"❌ Error starting Streamlit: {e}")\n\
        sys.exit(1)\n\
\n\
if __name__ == "__main__":\n\
    main()' > /app/start_streamlit.py

# Expose the port (Railway will override with $PORT)
EXPOSE $PORT

# Use the Python startup script
CMD ["python", "/app/start_streamlit.py"]
