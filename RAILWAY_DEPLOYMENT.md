# Railway Deployment Guide for Lost and Found API

## Issues Fixed

### ✅ Problem 1: Empty requirements.txt
**Issue**: The `backend/requirements.txt` file was empty, causing build failures.
**Solution**: Added all required dependencies:
- FastAPI and uvicorn for the web server
- pymongo for MongoDB connection
- Pillow and numpy for image processing
- google-generativeai for AI classification
- Other utility packages

### ✅ Problem 2: Empty railway.toml
**Issue**: No Railway configuration file.
**Solution**: Added proper Railway configuration with:
- Dockerfile build settings
- Health check endpoint (/health)
- Environment variables

### ✅ Problem 3: Dockerfile path issues
**Issue**: Incorrect file paths in Docker build.
**Solution**: Fixed COPY paths and import statements.

## Deployment Steps

### 1. Environment Variables
Set these in your Railway project dashboard:

**Required:**
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=lost_and_found
```

**Optional:**
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. MongoDB Setup
1. Create a free MongoDB Atlas account at https://cloud.mongodb.com/
2. Create a new cluster
3. Get your connection string
4. Add it to Railway environment variables

### 3. Deploy
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the `railway.toml` file
3. It will build using the Dockerfile
4. Health check endpoint: `https://your-app.railway.app/health`

### 4. API Endpoints
Once deployed, your API will be available at:
- Health check: `GET /health`
- Report item: `POST /report/`
- Get items: `GET /items/`
- Search: `GET /search/`

## Troubleshooting

### Build Failures
- Check Railway build logs for dependency installation errors
- Ensure all environment variables are set
- Verify MongoDB connection string is correct

### Runtime Errors
- Check Railway deployment logs
- Test the `/health` endpoint first
- Ensure MongoDB Atlas allows connections from Railway (0.0.0.0/0)

### Database Connection
- MongoDB Atlas requires whitelisting IP addresses
- Add `0.0.0.0/0` to allow connections from Railway
- Test connection string locally first

## File Structure for Railway
```
lost-and-found/
├── railway.toml          # Railway configuration
├── .railwayignore       # Files to exclude from deployment
├── .env.railway         # Environment variables template
└── backend/
    ├── Dockerfile       # Docker build instructions
    ├── requirements.txt # Python dependencies
    ├── main.py         # FastAPI application
    └── ... (other backend files)
```
