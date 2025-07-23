from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import sqlite3

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend import db, image_utils, gemini_api
    from backend.model import ReportItem
except ImportError:
    # Fallback to local imports
    import db, image_utils, gemini_api
    from model import ReportItem

app = FastAPI(title="Lost and Found API", version="1.0.0")

# Initialize database
try:
    db.init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

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
        image_path = None
        category = "Uncategorized"

        # Handle file upload
        if file:
            # Validate file type
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are allowed")
            
            image_path = image_utils.save_image(file)
            if image_path:
                category = gemini_api.classify_image(image_path)

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

        # Save to database
        db.insert_item(item, image_path)
        return {"message": "Item reported successfully", "category": category}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reporting item: {str(e)}")

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
        
        # Save uploaded image temporarily
        temp_image_path = image_utils.save_image(file)
        
        # Get all items from database
        all_items = db.fetch_all_items()
        
        # Extract image paths
        image_paths = [item[8] for item in all_items if item[8] and os.path.exists(item[8])]
        
        # Find similar images
        similar_images = image_utils.find_similar_images(temp_image_path, image_paths, threshold=0.1)
        
        # Match similar images with database items
        similar_items = []
        for img_path, similarity in similar_images[:10]:  # Top 10 matches
            for item in all_items:
                if item[8] == img_path:
                    item_with_similarity = list(item) + [similarity]
                    similar_items.append(item_with_similarity)
                    break
        
        # Clean up temporary image
        try:
            os.remove(temp_image_path)
        except:
            pass
            
        return {"items": similar_items, "count": len(similar_items)}
        
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
    return {"status": "healthy"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        success = db.delete_item(item_id)
        if success:
            return {"message": f"Item with ID {item_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)