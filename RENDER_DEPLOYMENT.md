# Render Deployment Guide - Lost and Found Portal

## 🚀 Why Render over Railway?

**Render is the better choice for your project because:**
- ✅ More generous free tier (750 hours/month)
- ✅ No credit card required for free tier  
- ✅ Simpler setup process
- ✅ Better suited for traditional web applications
- ✅ Excellent auto-deploy from GitHub

## 📋 Prerequisites

1. **MongoDB Atlas Account** (Free)
   - Sign up at: https://cloud.mongodb.com/
   - Create a cluster and get connection string

2. **GitHub Repository** 
   - Push your code to GitHub
   - Make sure it's public or you have Render access

3. **Google Gemini API** (Optional)
   - Get API key from: https://makersuite.google.com/app/apikey

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Your Repository
Your `render.yaml` file is already created. Make sure these files exist:
- ✅ `backend/requirements.txt` - Dependencies
- ✅ `backend/main.py` - FastAPI app  
- ✅ `render.yaml` - Render configuration

### Step 2: Deploy to Render
1. Go to https://render.com and sign up
2. Connect your GitHub account
3. Click "New Blueprint" 
4. Select your repository
5. Render will detect the `render.yaml` file automatically

### Step 3: Set Environment Variables
In Render dashboard, set these environment variables:

**Required:**
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=lost_and_found
```

**Optional:**
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 4: MongoDB Atlas Setup
1. In MongoDB Atlas dashboard:
   - Go to Network Access
   - Add IP Address: `0.0.0.0/0` (Allow access from anywhere)
   - Or add Render's IP ranges

2. Get your connection string:
   - Go to Database → Connect → Connect your application
   - Copy the connection string
   - Replace `<password>` with your actual password

## 🎨 Frontend Deployment (Streamlit Cloud)

### Option A: Streamlit Cloud (Recommended)
1. Go to https://share.streamlit.io/
2. Connect your GitHub account
3. Deploy from `frontend/app.py`
4. Set environment variable:
   ```
   API_URL=https://your-render-app-name.onrender.com
   ```

### Option B: Render Web Service
If you prefer everything on Render:

1. Create another web service on Render
2. Build command: `pip install -r frontend/requirements.txt`
3. Start command: `streamlit run frontend/app.py --server.port $PORT`
4. Environment variables:
   ```
   API_URL=https://your-backend-app.onrender.com
   ```

## 🔍 Testing Your Deployment

### 1. Test Backend API
- Health check: `https://your-app.onrender.com/health`
- API docs: `https://your-app.onrender.com/docs`

### 2. Test Frontend
- Open your Streamlit app URL
- Try uploading an image and reporting an item
- Check if images display correctly

## 🐛 Troubleshooting

### Backend Issues:
- Check Render logs in dashboard
- Verify MongoDB connection string
- Test `/health` endpoint first

### Frontend Issues:
- Update `API_URL` to your Render backend URL
- Check CORS settings in FastAPI
- Verify image loading from GridFS

### Database Issues:
- Ensure MongoDB Atlas allows connections from `0.0.0.0/0`
- Test connection string locally first
- Check database name matches environment variable

## 📝 Next Steps

1. **Deploy Backend First**: Get FastAPI running on Render
2. **Test API Endpoints**: Use `/docs` to test functionality  
3. **Deploy Frontend**: Use backend URL in Streamlit
4. **Test Full Flow**: Report items and search functionality
5. **Optional**: Set up custom domain

## 💡 Pro Tips

- Use Render's auto-deploy feature for continuous deployment
- Monitor usage to stay within free tier limits
- Set up MongoDB Atlas monitoring for database performance
- Consider upgrading to paid plans for production use

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com/
- MongoDB Atlas: https://cloud.mongodb.com/
- Streamlit Cloud: https://share.streamlit.io/
- Your API Documentation: `https://your-app.onrender.com/docs`
