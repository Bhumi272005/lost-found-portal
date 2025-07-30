# Deployment Guide for Lost & Found Portal

## 📦 Required Files for Deployment

### Core Files
- `requirements.txt` - Python package dependencies
- `packages.txt` - System packages for Streamlit Cloud
- `runtime.txt` - Python version specification
- `Procfile` - Process definition for Heroku
- `setup.sh` - Setup script for Streamlit Cloud
- `.streamlit/config.toml` - Streamlit configuration

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended for Frontend)

#### Prerequisites:
- GitHub repository with your code
- Streamlit Cloud account (free at share.streamlit.io)

#### Steps:
1. **Push code to GitHub**
2. **Connect Streamlit Cloud to your repository**
3. **Set environment variables:**
   ```
   MONGO_URL=your_mongodb_atlas_connection_string
   DATABASE_NAME=lost_and_found
   BASE_URL=https://your-app-name.streamlit.app
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. **Deploy automatically**

#### Required Files:
- ✅ `requirements.txt`
- ✅ `packages.txt`
- ✅ `.streamlit/config.toml`
- ✅ Frontend entry point: `frontend/app.py`

### 2. Heroku (Full Stack)

#### Prerequisites:
- Heroku account
- Heroku CLI installed

#### Steps:
1. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables:**
   ```bash
   heroku config:set MONGO_URL=your_mongodb_connection
   heroku config:set DATABASE_NAME=lost_and_found
   heroku config:set BASE_URL=https://your-app-name.herokuapp.com
   heroku config:set GEMINI_API_KEY=your_api_key
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

#### Required Files:
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`

### 3. Railway (Alternative)

#### Steps:
1. Connect Railway to your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

### 4. Render (Alternative)

#### Steps:
1. Connect Render to your GitHub repository
2. Configure build and start commands
3. Set environment variables

## 🔧 Environment Variables Required

### For All Platforms:
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=lost_and_found
BASE_URL=https://your-deployed-url.com
GEMINI_API_KEY=your_gemini_api_key_here
API_URL=https://your-api-url.com
```

## 📋 Pre-Deployment Checklist

### ✅ Code Preparation:
- [ ] All imports use relative paths
- [ ] Environment variables are properly configured
- [ ] No hardcoded localhost URLs
- [ ] Error handling is implemented
- [ ] Requirements.txt is complete

### ✅ MongoDB Setup:
- [ ] MongoDB Atlas cluster is created
- [ ] Database user is configured
- [ ] Network access is set to 0.0.0.0/0 (allow all)
- [ ] Connection string is obtained

### ✅ Gemini API:
- [ ] Google Cloud project is created
- [ ] Gemini API is enabled
- [ ] API key is generated
- [ ] Billing is enabled (if required)

### ✅ Files Check:
- [ ] `requirements.txt` exists and is complete
- [ ] `packages.txt` exists (for Streamlit Cloud)
- [ ] `runtime.txt` specifies Python version
- [ ] `.streamlit/config.toml` is configured
- [ ] `Procfile` is set up (for Heroku)

## 🚨 Common Deployment Issues

### 1. Import Errors
**Problem:** `ModuleNotFoundError`
**Solution:** Check requirements.txt and ensure all packages are listed

### 2. MongoDB Connection Issues
**Problem:** Can't connect to database
**Solution:** 
- Use MongoDB Atlas (cloud)
- Update connection string
- Check network access settings

### 3. File Path Issues
**Problem:** `FileNotFoundError` for images
**Solution:** Use relative paths and GridFS for image storage

### 4. Environment Variables
**Problem:** Configuration not loading
**Solution:** Set environment variables in platform dashboard

### 5. Port Issues
**Problem:** App not accessible
**Solution:** Use `$PORT` environment variable from platform

## 📱 Platform-Specific Notes

### Streamlit Cloud:
- Automatically installs from requirements.txt
- Uses packages.txt for system packages
- Limited to 1GB RAM
- Good for frontend-only apps

### Heroku:
- Uses Procfile for process definition
- Supports multiple processes (web + worker)
- Good for full-stack applications
- Free tier has sleep mode

### Railway/Render:
- Modern alternatives to Heroku
- Better performance on free tiers
- Easier configuration

## 🔄 Continuous Deployment

### GitHub Actions (Optional):
Create `.github/workflows/deploy.yml` for automated deployment:

```yaml
name: Deploy to Production
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to platform
        run: # Platform-specific deployment commands
```

## 🎯 Deployment Success Verification

After deployment, verify:
1. ✅ Frontend loads without errors
2. ✅ Backend API endpoints respond
3. ✅ Database connection works
4. ✅ Image upload and display functions
5. ✅ AI classification works
6. ✅ Search functionality works
7. ✅ Cross-computer access works

## 📞 Support

If you encounter issues:
1. Check platform logs for error messages
2. Verify environment variables
3. Test MongoDB connection
4. Check API key validity
5. Review requirements.txt completeness

---

**🎉 Ready for deployment with all necessary files included!**
