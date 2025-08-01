from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import io
import tempfile
import contextlib
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# For production, also try to load .env.production
if os.path.exists(".env.production"):
    load_dotenv(".env.production", override=True)

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend import mongodb as db, image_utils, gemini_api
    from backend.model import ReportItem
except ImportError:
    # Fallback to local imports
    import mongodb as db, image_utils, gemini_api
    from model import ReportItem

app = FastAPI(title="Lost and Found API", version="1.0.0")

# Clean up any existing temporary files on startup
def cleanup_temp_files():
    """Clean up any temporary files from previous runs"""
    try:
        current_dir = os.getcwd()
        for filename in os.listdir(current_dir):
            if filename.startswith("temp_") and filename.endswith(".jpg"):
                try:
                    os.remove(filename)
                    print(f"✅ Cleaned up temporary file: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not remove temporary file {filename}: {e}")
    except Exception as e:
        print(f"Error during temp file cleanup: {e}")

# Cleanup temp files on startup
cleanup_temp_files()

@contextlib.contextmanager
def temporary_image_file(image_data: bytes, file_id: str):
    """Context manager for handling temporary image files safely"""
    temp_path = f"temp_{file_id}.jpg"
    try:
        with open(temp_path, "wb") as temp_file:
            temp_file.write(image_data)
        yield temp_path
    finally:
        # Clean up temporary file with retry mechanism
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    time.sleep(0.1)  # Wait 100ms before retry
                    continue
                else:
                    print(f"Warning: Could not delete temporary file {temp_path} after {max_retries} attempts")
            except Exception as e:
                print(f"Error deleting temporary file {temp_path}: {e}")
                break

# Remove static files mount since we're using GridFS
# Images will be served through API endpoints

# Initialize MongoDB database
try:
    db.init_db()
    print("✅ MongoDB initialized successfully")
except Exception as e:
    print(f"❌ MongoDB initialization error: {e}")
    print("💡 Please ensure MongoDB is running or configure MongoDB Atlas")
    raise e

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/report/")
async def report_item(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    status: str = Form(...),
    name: str = Form("Anonymous"),
    contact: str = Form(...),
    file: UploadFile = None
):
    try:
        image_file_id = None
        category = "Uncategorized"

        # Handle file upload to GridFS
        if file:
            # Validate file type
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are allowed")
            
            # Read image data
            image_data = await file.read()
            
            # Store image in GridFS and get file ID
            image_file_id = db.store_image(image_data, file.filename)
            
            # For AI classification, use context manager for temporary file
            try:
                with temporary_image_file(image_data, image_file_id) as temp_path:
                    category = gemini_api.classify_image(temp_path)
            except Exception as e:
                print(f"Error in image classification: {e}")
                category = "Uncategorized"

        # Create item
        item = ReportItem(
            title=title,
            description=description,
            location=location,
            status=status,
            name=name,
            contact=contact,
            category=category
        )

        # Save to database with image data
        db.insert_item(item, image_data if file else None, file.filename if file else None)
        return {"message": "Item reported successfully", "category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reporting item: {str(e)}")

@app.get("/images/{file_id}")
async def get_image(file_id: str):
    """Serve images from GridFS"""
    try:
        image_data = db.get_image(file_id)
        if image_data:
            return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")

@app.get("/items/")
def get_items():
    try:
        items = db.fetch_all_items()
        return {"items": items, "count": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")

@app.post("/search/visual/")
async def visual_search(file: UploadFile):
    """Search for visually similar items using uploaded image"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        # Note: Visual search temporarily disabled for GridFS migration
        # TODO: Implement visual search with GridFS images
        return {"items": [], "count": 0, "message": "Visual search temporarily unavailable with GridFS storage"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in visual search: {str(e)}")

@app.get("/search/")
def search_items(q: str = "", status: str = "All"):
    try:
        if not q:
            # If no query, return all items
            items = db.fetch_all_items()
        else:
            items = db.search_items(q, status if status != "All" else None)
        return {"items": items, "count": len(items), "query": q}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching items: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Lost and Found API is running"}

@app.get("/health")
def health_check():
    """Health check endpoint that doesn't require database connection"""
    try:
        # Basic health check without database dependency
        return {
            "status": "healthy", 
            "service": "Lost and Found API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.get("/health/full")
def full_health_check():
    """Comprehensive health check including database connectivity"""
    try:
        # Test database connection
        db.client.admin.command('ping')
        database_status = "connected"
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if database_status == "connected" else "degraded",
        "database": database_status,
        "storage": "GridFS",
        "service": "Lost and Found API",
        "timestamp": datetime.now().isoformat()
    }


@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    try:
        success = db.delete_item(item_id)
        if success:
            return {"message": f"Item with ID {item_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")

@app.post("/admin/cleanup-temp-files")
def cleanup_temp_files_endpoint():
    """Admin endpoint to manually cleanup temporary files"""
    try:
        cleanup_temp_files()
        return {"message": "Temporary files cleanup completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during cleanup: {str(e)}")

@app.get("/api/items-with-urls")
def get_items_with_urls():
    """Get all items with shareable image URLs"""
    try:
        items = db.fetch_all_items_with_urls()
        return {"items": items, "count": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")

@app.post("/api/search-by-image-url")
def search_by_image_url(request: dict):
    """Search for similar items using image URL"""
    try:
        image_url = request.get("image_url")
        if not image_url:
            raise HTTPException(status_code=400, detail="image_url is required")
        
        results = db.search_by_image_url(image_url)
        return {
            "message": "Image search completed",
            "results": results,
            "count": len(results),
            "query_url": image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in image search: {str(e)}")

@app.get("/api/classify-image")
def classify_image_endpoint(image_url: str):
    """Classify an image from URL using Gemini AI"""
    try:
        from backend.gemini_api import classify_image_from_url
        
        if not image_url:
            raise HTTPException(status_code=400, detail="image_url parameter is required")
        
        category = classify_image_from_url(image_url)
        return {
            "image_url": image_url,
            "category": category,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)