# Railway Deployment Instructions

## ⚠️ IMPORTANT: Deploy Backend, Not Frontend

This repository contains:
- **FastAPI Backend** (`backend/main.py`) - Deploy this to Railway ✅
- **Streamlit Frontend** (`streamlit_app.py`) - Deploy this to Streamlit Cloud ❌

## Railway Configuration

Railway should use:
- **Dockerfile**: Builds FastAPI backend
- **Health endpoint**: `/health` (FastAPI provides this)
- **Start command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## Required Environment Variables

Set these in Railway dashboard:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/lost_and_found
DATABASE_NAME=lost_and_found
GEMINI_API_KEY=your-gemini-api-key
BASE_URL=https://your-app-name.railway.app
```

## Deployment Architecture

```
Railway (Backend)  ←→  Streamlit Cloud (Frontend)
FastAPI + MongoDB      Streamlit UI
```
