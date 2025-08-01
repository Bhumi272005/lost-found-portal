# Deployment Guide for Lost and Found Portal

## Making Image URLs Globally Shareable

### Step 1: Choose a Cloud Platform

#### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

#### Option B: Render
1. Go to [render.com](https://render.com)
2. Connect your GitHub account
3. Click "New" → "Web Service"
4. Select your repository

#### Option C: Heroku
1. Go to [heroku.com](https://heroku.com)
2. Create new app
3. Connect to GitHub repository

### Step 2: Set Up MongoDB Atlas (Cloud Database)

1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create free cluster
3. Get connection string like:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/lost_and_found
   ```

### Step 3: Configure Environment Variables

Set these in your cloud platform:

```bash
# MongoDB
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/lost_and_found?retryWrites=true&w=majority
DATABASE_NAME=lost_and_found

# Base URL (your deployed app URL)
BASE_URL=https://your-app-name.railway.app

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Optional: CORS
ALLOWED_ORIGINS=*
```

### Step 4: Deploy

1. Push your code to GitHub
2. Your cloud platform will automatically deploy
3. Get your app URL (e.g., `https://your-app.railway.app`)

### Step 5: Update BASE_URL

After deployment, update the `BASE_URL` environment variable to your actual deployed URL.

### Result

Your image URLs will now look like:
```
https://your-app.railway.app/images/64f7b8c9e4b0a1b2c3d4e5f6
```

These URLs will be accessible from **anywhere in the world**! 🌍

### Testing

1. Deploy your app
2. Create a test item with image
3. Check MongoDB - the `image_url` field should contain your global URL
4. Test the URL from any device/location

## Files Created/Modified

- `Dockerfile` - Container configuration
- `railway.json` - Railway deployment config  
- `.env.production` - Production environment template
- Updated `mongodb.py` - Better BASE_URL handling
- Updated `main.py` - Environment configuration
