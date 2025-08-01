# Lost & Found Portal - Streamlit Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
1. A running backend API (FastAPI) deployed on Heroku, Railway, or similar platform
2. GitHub repository with your code

### Steps to Deploy on Streamlit Cloud

1. **Push your code to GitHub** including the new `streamlit_app.py` file

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Connect your GitHub repository**

4. **Set the main file path to**: `streamlit_app.py`

5. **Configure Secrets** in Streamlit Cloud dashboard:
   ```toml
   API_URL = "https://your-backend-api-url.herokuapp.com"
   ADMIN_PASSWORD = "your-secure-admin-password"
   ```

6. **Deploy!**

### Troubleshooting Common Issues

#### 1. **Requirements Installation Error**
- Make sure your `requirements.txt` only contains frontend dependencies
- Remove backend-specific packages like `fastapi`, `uvicorn`, `pymongo`, etc.

#### 2. **Module Import Errors**
- Ensure all imports in `streamlit_app.py` are available in requirements.txt
- Check that there are no relative imports to backend modules

#### 3. **API Connection Issues**
- Verify your backend API is deployed and accessible
- Check that the API_URL in secrets matches your backend URL
- Ensure CORS is properly configured in your backend

#### 4. **Python Version Issues**
- Streamlit Cloud uses Python 3.9+ by default
- Make sure all packages in requirements.txt are compatible

### Backend Deployment (FastAPI)

Your backend needs to be deployed separately. Recommended platforms:

1. **Heroku** - Easy deployment with free tier
2. **Railway** - Modern alternative to Heroku
3. **DigitalOcean App Platform** - Good performance
4. **AWS/Google Cloud** - More advanced options

### Environment Variables for Backend

When deploying your backend, make sure to set:
- `MONGODB_URL` - Your MongoDB connection string
- `GEMINI_API_KEY` - Your Google Gemini API key
- Any other environment variables your backend needs

### File Structure After Updates

```
lost-found-portal/
├── streamlit_app.py          # Main Streamlit app (NEW)
├── requirements.txt          # Updated for frontend only
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── secrets.toml.template    # Template for secrets
├── frontend/
│   └── app.py              # Original frontend (keep for reference)
├── backend/                # Backend files (deploy separately)
│   ├── main.py
│   ├── model.py
│   └── ...
└── README.md               # This file
```

### Next Steps

1. Deploy your backend API first
2. Update the API_URL in Streamlit secrets
3. Test the deployment
4. Configure custom domain (optional)

### Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify backend API is running
3. Test API endpoints manually
4. Check browser console for errors
