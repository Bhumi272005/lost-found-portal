from pymongo import MongoClient
from datetime import datetime
import pytz
import os
import gridfs
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lost_and_found")
COLLECTION_NAME = "items"

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.fs = None  # GridFS for image storage
        # Use environment variable for base URL, fallback to localhost for development
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")  # Configurable base URL for global access
        self.connect()
    
    def connect(self):
        """Connect to MongoDB with improved error handling"""
        try:
            self.client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            self.fs = gridfs.GridFS(self.db)  # Initialize GridFS
            # Test the connection with timeout
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB at {MONGO_URL}")
            print("✅ GridFS initialized for image storage")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print("💡 Make sure MongoDB is running or use MongoDB Atlas cloud service")
            print("⚠️  API will start but database operations will fail until connection is established")
            # Don't raise the exception - let the app start without DB connection
            self.client = None
            self.db = None
            self.collection = None
            self.fs = None
    
    def get_ist_timestamp(self):
        """Get current timestamp in Indian Standard Time"""
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    
    def format_ist_timestamp(self, timestamp):
        """Format timestamp to display IST time clearly"""
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            # Convert to IST
            ist = pytz.timezone('Asia/Kolkata')
            if dt.tzinfo is None:
                dt = pytz.utc.localize(dt)
            dt_ist = dt.astimezone(ist)
            return dt_ist.strftime('%d-%m-%Y %H:%M:%S IST')
        except:
            return str(timestamp) + ' IST'
    
    def store_image(self, image_data: bytes, filename: str) -> str:
        """Store image in GridFS and return the file ID"""
        try:
            file_id = self.fs.put(image_data, filename=filename)
            return str(file_id)
        except Exception as e:
            print(f"Error storing image in GridFS: {e}")
            raise e
    
    def get_image(self, file_id: str) -> bytes:
        """Retrieve image from GridFS by file ID"""
        try:
            from bson import ObjectId
            grid_out = self.fs.get(ObjectId(file_id))
            return grid_out.read()
        except Exception as e:
            print(f"Error retrieving image from GridFS: {e}")
            return None
    
    def delete_image(self, file_id: str) -> bool:
        """Delete image from GridFS"""
        try:
            from bson import ObjectId
            self.fs.delete(ObjectId(file_id))
            return True
        except Exception as e:
            print(f"Error deleting image from GridFS: {e}")
            return False
    
    def generate_image_url(self, file_id: str) -> str:
        """Generate shareable URL for image"""
        if not file_id:
            return None
        return f"{self.base_url}/images/{file_id}"
    
    def insert_item(self, item, image_data: bytes = None, image_filename: str = None) -> str:
        """Insert a new item into the database with image stored in GridFS and AI classification"""
        try:
            image_file_id = None
            ai_category = None
            image_url = None
            
            if image_data and image_filename:
                # Store image in GridFS
                image_file_id = self.store_image(image_data, image_filename)
                image_url = self.generate_image_url(image_file_id)
                
                # Use Gemini API to classify the image
                try:
                    from backend.gemini_api import classify_image_from_bytes
                    ai_category = classify_image_from_bytes(image_data)
                    print(f"AI classified image as: {ai_category}")
                except Exception as e:
                    print(f"AI classification failed: {e}")
                    ai_category = "Uncategorized"
            
            document = {
                "title": item.title,
                "description": item.description,
                "category": item.category,
                "ai_category": ai_category,  # Store AI classification
                "location": item.location,
                "status": item.status,
                "name": item.name,
                "contact": item.contact,
                "image_file_id": image_file_id,  # Store GridFS file ID instead of path
                "image_url": image_url,  # Store shareable URL
                "timestamp": self.get_ist_timestamp()
            }
            
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting item: {e}")
            raise e
    
    def fetch_all_items(self) -> List[tuple]:
        """Fetch all items from the database"""
        try:
            cursor = self.collection.find().sort("timestamp", -1)
            items = []
            
            for doc in cursor:
                # Convert MongoDB document to tuple format similar to SQLite
                item_tuple = (
                    str(doc["_id"]),  # id
                    doc.get("title", ""),
                    doc.get("description", ""),
                    doc.get("category", ""),
                    doc.get("location", ""),
                    doc.get("status", ""),
                    doc.get("name", ""),
                    doc.get("contact", ""),
                    doc.get("image_file_id", ""),  # GridFS file ID instead of path
                    self.format_ist_timestamp(doc.get("timestamp", ""))
                )
                items.append(item_tuple)
            
            return items
        except Exception as e:
            print(f"Error fetching items: {e}")
            return []
    
    def search_items(self, query: str, status_filter: Optional[str] = None) -> List[tuple]:
        """Search items by title, description, or category"""
        try:
            # Build search filter
            search_filter = {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"category": {"$regex": query, "$options": "i"}}
                ]
            }
            
            # Add status filter if provided
            if status_filter and status_filter != "All":
                search_filter["status"] = status_filter
            
            cursor = self.collection.find(search_filter).sort("timestamp", -1)
            items = []
            
            for doc in cursor:
                item_tuple = (
                    str(doc["_id"]),
                    doc.get("title", ""),
                    doc.get("description", ""),
                    doc.get("category", ""),
                    doc.get("location", ""),
                    doc.get("status", ""),
                    doc.get("name", ""),
                    doc.get("contact", ""),
                    doc.get("image_file_id", ""),  # GridFS file ID
                    self.format_ist_timestamp(doc.get("timestamp", ""))
                )
                items.append(item_tuple)
                
            return items
        except Exception as e:
            print(f"Error searching items: {e}")
            return []
    
    def delete_item(self, item_id: str) -> bool:
        """Delete an item by ID"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a single item by ID"""
        try:
            from bson import ObjectId
            doc = self.collection.find_one({"_id": ObjectId(item_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
                doc["timestamp"] = self.format_ist_timestamp(doc.get("timestamp", ""))
            return doc
        except Exception as e:
            print(f"Error getting item by ID: {e}")
            return None
    
    def fetch_all_items_with_urls(self) -> List[Dict]:
        """Fetch all items with image URLs instead of tuples"""
        try:
            cursor = self.collection.find().sort("timestamp", -1)
            items = []
            
            for doc in cursor:
                item_dict = {
                    "id": str(doc["_id"]),
                    "title": doc.get("title", ""),
                    "description": doc.get("description", ""),
                    "category": doc.get("category", ""),
                    "ai_category": doc.get("ai_category", ""),
                    "location": doc.get("location", ""),
                    "status": doc.get("status", ""),
                    "name": doc.get("name", ""),
                    "contact": doc.get("contact", ""),
                    "image_file_id": doc.get("image_file_id", ""),
                    "image_url": self.generate_image_url(doc.get("image_file_id")),
                    "timestamp": self.format_ist_timestamp(doc.get("timestamp", ""))
                }
                items.append(item_dict)
            
            return items
        except Exception as e:
            print(f"Error fetching items: {e}")
            return []
    
    def search_by_image_url(self, image_url: str) -> List[Dict]:
        """Search for similar items using image URL and AI classification"""
        try:
            from backend.gemini_api import classify_image_from_url
            
            # Classify the search image
            search_category = classify_image_from_url(image_url)
            print(f"Search image classified as: {search_category}")
            
            # Search for items with similar AI categories
            search_filter = {
                "$or": [
                    {"ai_category": {"$regex": search_category, "$options": "i"}},
                    {"category": {"$regex": search_category, "$options": "i"}},
                    {"title": {"$regex": search_category, "$options": "i"}},
                    {"description": {"$regex": search_category, "$options": "i"}}
                ]
            }
            
            cursor = self.collection.find(search_filter).sort("timestamp", -1)
            items = []
            
            for doc in cursor:
                item_dict = {
                    "id": str(doc["_id"]),
                    "title": doc.get("title", ""),
                    "description": doc.get("description", ""),
                    "category": doc.get("category", ""),
                    "ai_category": doc.get("ai_category", ""),
                    "location": doc.get("location", ""),
                    "status": doc.get("status", ""),
                    "name": doc.get("name", ""),
                    "contact": doc.get("contact", ""),
                    "image_file_id": doc.get("image_file_id", ""),
                    "image_url": self.generate_image_url(doc.get("image_file_id")),
                    "timestamp": self.format_ist_timestamp(doc.get("timestamp", ""))
                }
                items.append(item_dict)
            
            return items
        except Exception as e:
            print(f"Error in image search: {e}")
            return []

    def list_all_images(self) -> List[Dict]:
        """List all images stored in GridFS with metadata"""
        try:
            files = []
            for grid_file in self.fs.find():
                files.append({
                    'file_id': str(grid_file._id),
                    'filename': grid_file.filename,
                    'upload_date': grid_file.upload_date,
                    'length': grid_file.length,
                    'content_type': getattr(grid_file, 'contentType', 'image/jpeg')
                })
            return files
        except Exception as e:
            print(f"Error listing images: {e}")
            return []

# Global MongoDB instance
mongodb_instance = None

def get_mongodb():
    """Get MongoDB instance (singleton pattern)"""
    global mongodb_instance
    if mongodb_instance is None:
        mongodb_instance = MongoDB()
    return mongodb_instance

# Wrapper functions to maintain compatibility with existing code
def init_db():
    """Initialize MongoDB connection"""
    get_mongodb()

def insert_item(item, image_data=None, image_filename=None):
    """Insert item using MongoDB with GridFS image storage"""
    return get_mongodb().insert_item(item, image_data, image_filename)

def fetch_all_items():
    """Fetch all items using MongoDB"""
    return get_mongodb().fetch_all_items()

def search_items(query, status_filter=None):
    """Search items using MongoDB"""
    return get_mongodb().search_items(query, status_filter)

def delete_item(item_id):
    """Delete item using MongoDB"""
    return get_mongodb().delete_item(item_id)

def get_item_by_id(item_id):
    """Get item by ID using MongoDB"""
    return get_mongodb().get_item_by_id(item_id)

def get_image(file_id):
    """Get image from GridFS"""
    return get_mongodb().get_image(file_id)

def store_image(image_data, filename):
    """Store image in GridFS"""
    return get_mongodb().store_image(image_data, filename)

def fetch_all_items_with_urls():
    """Fetch all items with URLs using MongoDB"""
    return get_mongodb().fetch_all_items_with_urls()

def search_by_image_url(image_url):
    """Search items by image URL using MongoDB"""
    return get_mongodb().search_by_image_url(image_url)

def list_all_images():
    """List all images using MongoDB"""
    return get_mongodb().list_all_images()
