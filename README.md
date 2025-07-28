# Lost & Found Portal

A web-based Lost & Found portal with FastAPI backend and Streamlit frontend, powered by **MongoDB with GridFS** for cross-computer image sharing.

## 🎯 Key Features

- 📝 Report lost/found items with image upload
- 🔍 Search functionality with text search
- 🏷️ AI-powered image classification using Google Gemini
- ⚙️ Admin panel for item management
- 🌐 **Multi-computer access** - Images stored in MongoDB GridFS
- 📱 Mobile-friendly interface
- 🖼️ **Shared image storage** - All computers can see the same images

## Prerequisites

**MongoDB is required** - Choose one option:

### Option 1: Local MongoDB
1. Install MongoDB Community Edition from https://www.mongodb.com/try/download/community
2. Create data directory: `mkdir data\db`
3. Start MongoDB: `mongod --dbpath data\db`

### Option 2: MongoDB Atlas (Cloud - Recommended)
1. Create free account at https://cloud.mongodb.com/
2. Create cluster and get connection string
3. Update `.env` file with your connection string

## Quick Start

### 1. Install Dependencies
```bash
.venv\Scripts\pip.exe install -r requirements.txt
```

### 2. Setup Environment
Update `.env` file:
```
MONGO_URL=mongodb://localhost:27017/  # or your Atlas connection string
DATABASE_NAME=lost_and_found
GEMINI_API_KEY=your_api_key_here      # Optional
```

### 3. Test MongoDB Connection
```bash
.venv\Scripts\python.exe setup_mongodb.py
```

### 4. Start Application

**Option A - Use VS Code Task (Recommended):**
- Press `Ctrl+Shift+P`
- Run "Tasks: Run Task"
- Select "Start Lost and Found API Server"
- Open http://localhost:8501 for frontend

**Option B - Manual Start:**
```bash
# Terminal 1 - Backend
.venv\Scripts\uvicorn.exe backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend  
.venv\Scripts\streamlit.exe run frontend\app.py
```

**Option C - Simple Script:**
```bash
.venv\Scripts\python.exe run.py
```
Frontend runs on: http://localhost:8501

## Configuration

Copy `.env.example` to `.env` and configure:

### For Local MongoDB:
```
MONGO_URL=mongodb://localhost:27017/
DATABASE_NAME=lost_and_found
```

### For MongoDB Atlas:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=lost_and_found
```

## Network Access

To access from other computers:
1. Find your IP: `ipconfig`
2. Allow port 8000 in Windows Firewall
3. Access via: `http://YOUR_IP:8000`

## Project Structure
```
├── backend/           # FastAPI backend
│   ├── main.py       # API server
│   ├── mongodb.py    # MongoDB database
│   └── ...
├── frontend/         # Streamlit frontend
│   └── app.py        # Web interface
├── images/           # Uploaded images
├── setup_mongodb.py  # MongoDB setup helper
└── requirements.txt  # Dependencies
```

## Project Structure
```
lost-and-found/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── db.py            # Database operations with IST support
│   ├── model.py         # Pydantic models
│   ├── gemini_api.py    # AI image classification
│   └── image_utils.py   # Image processing utilities
├── frontend/
│   └── app.py           # Streamlit application
├── images/              # Uploaded images storage
├── database.db          # SQLite database
├── requirements.txt     # Python dependencies
├── run_frontend.py      # Frontend runner script
└── README.md           # This documentation
```
