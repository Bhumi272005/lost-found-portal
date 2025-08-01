#!/usr/bin/env python3
"""
Python script to check image URL shareability in Lost and Found database
This script connects to your MongoDB and analyzes image URLs
"""

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# MongoDB connection settings
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lost_and_found")

def check_image_urls():
    """Check if image URLs in database are shareable"""
    
    try:
        # Connect to MongoDB
        print("🔗 Connecting to MongoDB...")
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        collection = db["items"]
        
        print(f"✅ Connected to database: {DATABASE_NAME}")
        print("=" * 50)
        
        # 1. Database statistics
        print("📊 DATABASE STATISTICS")
        total_items = collection.count_documents({})
        items_with_images = collection.count_documents({"image_url": {"$exists": True, "$ne": None}})
        
        print(f"Total items: {total_items}")
        print(f"Items with images: {items_with_images}")
        print()
        
        if items_with_images == 0:
            print("❌ No items with images found!")
            return
        
        # 2. Sample items with images
        print("🖼️  SAMPLE ITEMS WITH IMAGES")
        sample_items = collection.find(
            {"image_url": {"$exists": True, "$ne": None}},
            {"title": 1, "image_url": 1, "status": 1, "timestamp": 1, "_id": 0}
        ).limit(5)
        
        for i, item in enumerate(sample_items, 1):
            print(f"{i}. Title: {item.get('title', 'N/A')}")
            print(f"   Status: {item.get('status', 'N/A')}")
            print(f"   Image URL: {item.get('image_url', 'N/A')}")
            print(f"   Timestamp: {item.get('timestamp', 'N/A')}")
            print()
        
        # 3. Analyze URL patterns
        print("🔍 IMAGE URL ANALYSIS")
        all_image_urls = collection.distinct("image_url")
        print(f"Total unique image URLs: {len(all_image_urls)}")
        
        # Count URL types
        localhost_count = 0
        network_count = 0
        global_count = 0
        
        for url in all_image_urls:
            if url and isinstance(url, str):
                if 'localhost' in url or '127.0.0.1' in url:
                    localhost_count += 1
                elif '192.168.' in url or '10.0.' in url or '172.' in url:
                    network_count += 1
                elif url.startswith('https://') and '192.168.' not in url and 'localhost' not in url:
                    global_count += 1
        
        print("URL Shareability Analysis:")
        print(f"❌ Localhost URLs (not shareable): {localhost_count}")
        print(f"⚠️  Local network URLs (limited sharing): {network_count}")
        print(f"✅ Global URLs (fully shareable): {global_count}")
        print()
        
        # 4. Show sample URLs
        print("📋 SAMPLE IMAGE URLS")
        for i, url in enumerate(all_image_urls[:3], 1):
            if url:
                print(f"{i}. {url}")
                
                # Determine shareability
                if 'localhost' in url or '127.0.0.1' in url:
                    print("   Status: ❌ Not shareable (localhost only)")
                elif '192.168.' in url or '10.0.' in url or '172.' in url:
                    print("   Status: ⚠️  Local network only")
                elif url.startswith('https://') and '192.168.' not in url and 'localhost' not in url:
                    print("   Status: ✅ Globally shareable")
                else:
                    print("   Status: ❓ Unknown pattern")
                print()
        
        # 5. Check GridFS
        print("💾 GRIDFS INFORMATION")
        try:
            gridfs_files = db["fs.files"].count_documents({})
            print(f"GridFS files stored: {gridfs_files}")
            
            if gridfs_files > 0:
                print("Sample GridFS files:")
                sample_files = db["fs.files"].find({}, {"filename": 1, "uploadDate": 1}).limit(3)
                for file_doc in sample_files:
                    print(f"- {file_doc.get('filename', 'Unknown')} ({file_doc.get('uploadDate', 'Unknown date')})")
        except Exception as e:
            print(f"GridFS check error: {e}")
        print()
        
        # 6. Recommendations
        print("🎯 RECOMMENDATIONS")
        if global_count == 0:
            print("🚀 RECOMMENDATION: Deploy to cloud platform (Railway, Heroku, etc.)")
            print("📋 Current URLs are only accessible locally/on your network")
            print("🔗 Follow the deployment guide in DEPLOYMENT.md")
        else:
            print("🎉 Great! You have globally shareable URLs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure MongoDB is running and accessible")
    
    finally:
        try:
            client.close()
            print("\n🔐 Database connection closed")
        except:
            pass

if __name__ == "__main__":
    print("🔍 Lost and Found - Image URL Shareability Checker")
    print("=" * 60)
    check_image_urls()
