# 🔍 Lost & Found Portal

A modern web application to help people find and report lost items with AI-powered image classification.

## 🌍 Live Demo
- **Frontend**: https://your-app.streamlit.app (Deploy to get URL)
- **Backend API**: https://your-project.up.railway.app (Deploy to get URL)

## ✨ Features
- 📝 Report lost/found items with photos
- 🔍 Search items by keywords and categories  
- 🤖 AI-powered image classification using Google Gemini
- 📱 Mobile-friendly responsive design
- 🌐 Global image URL sharing
- ☁️ Cloud-based storage and deployment

## 🏗️ Architecture
- **Frontend**: Streamlit (deployed on Streamlit Cloud)
- **Backend**: FastAPI (deployed on Railway)
- **Database**: MongoDB Atlas (cloud)
- **Image Storage**: GridFS with global CDN
- **AI**: Google Gemini API for image classification

## 📁 Project Structure
```
lost-found-portal/
├── 📂 backend/           # FastAPI Backend
│   ├── main.py          # FastAPI application
│   ├── mongodb.py       # Database connection & operations
│   ├── model.py         # Data models
│   ├── gemini_api.py    # AI image classification
│   ├── image_utils.py   # Image processing utilities
│   └── requirements.txt # Python dependencies
├── 📂 frontend/         # Streamlit Frontend
│   ├── .streamlit/
│   │   └── secrets.toml # Configuration secrets
│   ├── main_app.py     # Main Streamlit application
│   └── requirements.txt # Frontend dependencies
├── 📄 Procfile         # Railway deployment config
├── 📄 railway.json     # Railway settings
├── 📄 runtime.txt      # Python version
├── 📄 .env.production  # Production environment template
└── 📄 README.md        # This file
```

## 🚀 Quick Deploy

### 1. Setup MongoDB Atlas
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create a free M0 cluster
3. Create database user and get connection string

### 2. Deploy Backend (Railway)
1. Go to [railway.app](https://railway.app)
2. Connect this GitHub repository
3. Add environment variables:
   ```env
   MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/
   DATABASE_NAME=lost_and_found
   BASE_URL=https://your-project.up.railway.app
   ALLOWED_ORIGINS=https://your-app.streamlit.app
   ```

### 3. Deploy Frontend (Streamlit Cloud)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect this GitHub repository
3. Set main file: `frontend/main_app.py`
4. Add secrets:
   ```toml
   [api]
   API_URL = "https://your-railway-project.up.railway.app"
   ```

## 🛠️ Local Development

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend  
pip install -r requirements.txt
streamlit run main_app.py
```

## 🔧 Environment Variables

### Backend (.env.production)
```env
MONGO_URL=mongodb+srv://...
DATABASE_NAME=lost_and_found
BASE_URL=https://your-project.up.railway.app
ALLOWED_ORIGINS=https://your-app.streamlit.app
GEMINI_API_KEY=your_api_key_here  # Optional for AI features
```

### Frontend (secrets.toml)
```toml
[api]
API_URL = "https://your-railway-project.up.railway.app"
```

## 📱 API Endpoints

- `GET /health` - Health check
- `GET /items/` - Get all items
- `POST /report/` - Report new item (with file upload)
- `GET /search/` - Search items by query
- `GET /images/{file_id}` - Serve images from GridFS
- `POST /search/visual/` - Visual similarity search
- `GET /docs` - Interactive API documentation

## 🌟 Key Features

### Global Image Sharing
Images are served via Railway's global CDN, making URLs accessible worldwide:
```
https://your-project.up.railway.app/images/abc123def456
```

### AI Classification
Automatic item categorization using Google Gemini Vision API for uploaded images.

### Real-time Search
Full-text search across item titles, descriptions, and categories.

### Mobile Responsive
Works seamlessly on desktop, tablet, and mobile devices.

## 🔒 Security Features
- HTTPS everywhere
- CORS protection
- Environment-based secrets
- Secure database authentication
- Input validation and sanitization

## 💰 Cost
- **MongoDB Atlas M0**: FREE (512MB)
- **Railway**: FREE tier (500 hours/month)
- **Streamlit Cloud**: FREE (unlimited public apps)
- **Total**: $0/month for personal use

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License
MIT License - see LICENSE file for details

---

Built with ❤️ using Python, FastAPI, Streamlit, and MongoDB
