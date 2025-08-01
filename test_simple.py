#!/usr/bin/env python3
"""
Simple FastAPI test for Railway deployment verification
"""
import os
from fastapi import FastAPI

app = FastAPI(title="Railway Test API")

@app.get("/")
def read_root():
    return {
        "message": "FastAPI is working on Railway!",
        "status": "ok",
        "port": os.getenv("PORT", "8000"),
        "service": "backend-only"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "FastAPI Backend"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting FastAPI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
