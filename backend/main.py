from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import io
import tempfile
import contextlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    allow_origins=["*"],
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
    return {"status": "healthy", "database": "MongoDB", "storage": "GridFS"}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)