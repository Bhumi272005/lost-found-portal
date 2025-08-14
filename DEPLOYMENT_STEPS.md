# 🚀 Frontend Deployment Guide for Streamlit Cloud

## ✅ Your Railway Backend is Ready!
**Backend URL**: https://lost-found-portal-production.up.railway.app

## 📋 Step 1: Set Railway Environment Variables

Go to your Railway project → Settings → Variables and add:

```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=lost_and_found
BASE_URL=https://lost-found-portal-production.up.railway.app
ALLOWED_ORIGINS=https://your-streamlit-app.streamlit.app,http://localhost:8501
GEMINI_API_KEY=your_gemini_api_key_here
```

## 📱 Step 2: Deploy Frontend to Streamlit Cloud

### 2.1 Go to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

### 2.2 Connect Repository
1. **Repository**: `Bhumi272005/lost-found-portal`
2. **Branch**: `main`
3. **Main file path**: `frontend/main_app.py`
4. **App URL**: Choose `lost-found-portal` or similar

### 2.3 Add Secrets
In Streamlit Cloud, go to App settings → Secrets and add:

```toml
[api]
API_URL = "https://lost-found-portal-production.up.railway.app"

[app]
title = "Lost & Found Portal"
```

### 2.4 Deploy
Click "Deploy!" and wait for deployment to complete.

## 🔄 Step 3: Update CORS Settings

Once you get your Streamlit URL (e.g., `https://lost-found-portal.streamlit.app`):

1. Go back to Railway → Settings → Variables
2. Update `ALLOWED_ORIGINS` to include your Streamlit URL:
   ```
   ALLOWED_ORIGINS=https://your-actual-streamlit-url.streamlit.app,http://localhost:8501
   ```

## ✅ Step 4: Test the Connection

1. **Test Backend**: Visit https://lost-found-portal-production.up.railway.app/health
2. **Test Frontend**: Visit your Streamlit app URL
3. **Test Integration**: Try reporting an item with an image

## 🌍 Step 5: Verify Global Image URLs

Your images will now be globally accessible at:
```
https://lost-found-portal-production.up.railway.app/images/{file_id}
```

These URLs will work from anywhere in the world! 🚀

## 🎯 Expected Result

- ✅ **Backend**: https://lost-found-portal-production.up.railway.app
- ✅ **Frontend**: https://your-app.streamlit.app  
- ✅ **Images**: Global URLs accessible worldwide
- ✅ **Database**: MongoDB Atlas cloud storage

Your Lost & Found Portal will be fully deployed and globally accessible! 🌟
