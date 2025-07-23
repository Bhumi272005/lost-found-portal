# Lost & Found Portal - Complete Application Guide

## Overview
This is a complete Lost & Found portal with a FastAPI backend and Streamlit frontend, featuring:
- 📝 Report lost/found items with image upload
- 🔍 Search functionality with text queries
- 🏷️ AI-powered image classification using Google Gemini
- ⚙️ Admin panel for item management
- 🕐 Indian Standard Time (IST) timestamps in 24-hour format
- 📱 Mobile-friendly interface

## Features

### 🔧 Backend (FastAPI)
- **REST API** with proper error handling
- **Database**: SQLite with IST timestamp support
- **Image Processing**: Automatic category detection using Google Gemini AI
- **File Upload**: Secure image handling with validation
- **Search**: Text-based search across title, description, and category
- **Admin Functions**: Delete items by ID

### 🎨 Frontend (Streamlit)
- **Three-page interface**: Search, Report, Admin
- **Real-time API health monitoring**
- **Image upload via camera or file picker**
- **Responsive design with status indicators**
- **Auto-refresh after operations**

## Setup Instructions

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up Gemini API (optional)
# Get API key from: https://makersuite.google.com/app/apikey
set GEMINI_API_KEY=your_actual_api_key

# Start the API server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup
```bash
# Run the frontend
streamlit run frontend/app.py
# OR
python run_frontend.py
```

### 3. Access the Application
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

### 4. Admin Access (For You)
- **Admin Password**: `admin123`
- **How to Login**: Click "🔐 Admin Login" in the sidebar
- **Admin Features**: Full access to Admin Panel with item management

## Quick Start Guide

### For Admin (You):
1. **Start Backend**: The API server should be running on port 8000
2. **Start Frontend**: Run `python start_frontend.py` or `streamlit run frontend/app.py`
3. **Access Admin Panel**: 
   - Open http://localhost:8501
   - Click "🔐 Admin Login" in sidebar
   - Enter password: `admin123`
   - Access all three pages including Admin Dashboard

### For Regular Users:
- Can access "🔍 Search Items" and "📝 Report Item" without authentication
- Cannot see or access Admin Panel

## API Endpoints

### Core Endpoints
- `GET /` - API status
- `GET /health` - Health check
- `GET /items/` - Fetch all items
- `GET /search/?q={query}&status={status}` - Search items
- `POST /report/` - Submit new item (multipart form)
- `DELETE /items/{id}` - Delete item by ID

### Search Parameters
- `q`: Search query (searches title, description, category)
- `status`: Filter by "Lost", "Found", or "All"

## Key Features

### 🔍 Search Functionality
- **Text Search**: Searches across item title, description, and category
- **Status Filter**: Filter by Lost/Found items
- **Real-time Results**: Instant search with result count

### 📝 Item Reporting
- **Dual Image Input**: Camera capture or file upload
- **AI Classification**: Automatic category detection using Google Gemini
- **Validation**: Required fields with proper error handling
- **Success Feedback**: Confirmation with auto-detected category display

### ⚙️ Admin Panel
- **Item Management**: View all items with full details
- **Delete Functionality**: Remove items with confirmation
- **Statistics**: Total item count display
- **Expandable Cards**: Clean, organized item display

### 🕐 Timestamp Handling
- **IST Timezone**: All timestamps in Indian Standard Time
- **24-hour Format**: DD-MM-YYYY HH:MM:SS IST format
- **Auto-generated**: Timestamps created on item submission

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
