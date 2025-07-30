"""
Image Viewer Utility for Lost & Found Portal
This script helps you view and export all images stored in MongoDB GridFS

Usage:
1. python view_images.py --list          # List all images with metadata
2. python view_images.py --export        # Export all images to local folder
3. python view_images.py --info <file_id># Get info about specific image
4. python view_images.py --view <file_id># Save specific image to view
"""

import os
import sys
import argparse
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.mongodb import get_mongodb
except ImportError:
    import mongodb
    get_mongodb = mongodb.get_mongodb

def list_all_images():
    """List all images stored in GridFS with metadata"""
    try:
        db = get_mongodb()
        
        print("🖼️  Lost & Found Portal - Image List")
        print("=" * 60)
        
        # Get all GridFS files
        files = []
        total_size = 0
        
        for grid_file in db.fs.find():
            file_info = {
                'file_id': str(grid_file._id),
                'filename': grid_file.filename or f"image_{grid_file._id}.jpg",
                'upload_date': grid_file.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'size': grid_file.length,
                'size_mb': round(grid_file.length / (1024*1024), 2)
            }
            files.append(file_info)
            total_size += grid_file.length
        
        if not files:
            print("📭 No images found in the database.")
            return
        
        print(f"📊 Total Images: {len(files)}")
        print(f"💾 Total Size: {round(total_size / (1024*1024), 2)} MB")
        print("\n" + "=" * 60)
        
        for i, file in enumerate(files, 1):
            print(f"\n{i}. 📷 {file['filename']}")
            print(f"   🆔 File ID: {file['file_id']}")
            print(f"   📅 Upload Date: {file['upload_date']}")
            print(f"   📦 Size: {file['size_mb']} MB")
            print(f"   🌐 View URL: http://localhost:8000/images/{file['file_id']}")
        
        print("\n" + "=" * 60)
        print("💡 To view an image:")
        print("   • Open the View URL in your browser")
        print("   • Or use: python view_images.py --view <file_id>")
        
    except Exception as e:
        print(f"❌ Error listing images: {e}")

def export_all_images():
    """Export all GridFS images to local folder"""
    try:
        db = get_mongodb()
        export_folder = "exported_images"
        
        # Create export folder
        os.makedirs(export_folder, exist_ok=True)
        
        print("📁 Exporting all images...")
        print(f"📂 Export folder: {os.path.abspath(export_folder)}")
        print("-" * 40)
        
        exported = 0
        
        for grid_file in db.fs.find():
            file_id = str(grid_file._id)
            filename = grid_file.filename or f"image_{file_id}.jpg"
            
            # Get image data
            image_data = db.get_image(file_id)
            if image_data:
                # Create safe filename
                safe_filename = "".join(c for c in filename if c.isalnum() or c in '.-_')
                if not safe_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    safe_filename += '.jpg'
                
                filepath = os.path.join(export_folder, f"{exported+1:03d}_{safe_filename}")
                
                with open(filepath, "wb") as f:
                    f.write(image_data)
                
                print(f"✅ Saved: {filepath}")
                exported += 1
            else:
                print(f"❌ Failed to get image: {filename}")
        
        print("-" * 40)
        print(f"🎉 Exported {exported} images to '{export_folder}' folder")
        print(f"📂 Open folder: {os.path.abspath(export_folder)}")
        
    except Exception as e:
        print(f"❌ Error exporting images: {e}")

def get_image_info(file_id):
    """Get detailed information about a specific image"""
    try:
        db = get_mongodb()
        
        from bson import ObjectId
        grid_file = db.fs.find_one({"_id": ObjectId(file_id)})
        
        if not grid_file:
            print(f"❌ Image not found with ID: {file_id}")
            return
        
        print("🖼️  Image Information")
        print("=" * 40)
        print(f"🆔 File ID: {file_id}")
        print(f"📁 Filename: {grid_file.filename or 'Unknown'}")
        print(f"📅 Upload Date: {grid_file.upload_date}")
        print(f"📦 File Size: {round(grid_file.length / 1024, 2)} KB")
        print(f"🏷️  Content Type: {getattr(grid_file, 'contentType', 'image/jpeg')}")
        print(f"🌐 View URL: http://localhost:8000/images/{file_id}")
        
        # Find associated item
        items = db.fetch_all_items()
        associated_item = None
        for item in items:
            if item[8] == file_id:  # image_file_id is at index 8
                associated_item = item
                break
        
        if associated_item:
            print("\n📝 Associated Item:")
            print(f"   Title: {associated_item[1]}")
            print(f"   Status: {associated_item[5]}")
            print(f"   Location: {associated_item[4]}")
            print(f"   Reported by: {associated_item[6]}")
        
    except Exception as e:
        print(f"❌ Error getting image info: {e}")

def view_single_image(file_id):
    """Save a single image to view locally"""
    try:
        db = get_mongodb()
        
        print(f"🔍 Retrieving image: {file_id}")
        
        # Get image data
        image_data = db.get_image(file_id)
        if not image_data:
            print(f"❌ Image not found with ID: {file_id}")
            return
        
        # Get filename from GridFS
        from bson import ObjectId
        grid_file = db.fs.find_one({"_id": ObjectId(file_id)})
        filename = grid_file.filename if grid_file else f"image_{file_id}.jpg"
        
        # Save to current directory
        safe_filename = f"view_{filename}"
        with open(safe_filename, "wb") as f:
            f.write(image_data)
        
        print(f"✅ Image saved as: {safe_filename}")
        print(f"📂 Full path: {os.path.abspath(safe_filename)}")
        print("💡 You can now open this file with any image viewer")
        
    except Exception as e:
        print(f"❌ Error viewing image: {e}")

def main():
    parser = argparse.ArgumentParser(description="Lost & Found Portal - Image Viewer Utility")
    parser.add_argument("--list", action="store_true", help="List all images with metadata")
    parser.add_argument("--export", action="store_true", help="Export all images to local folder")
    parser.add_argument("--info", type=str, help="Get info about specific image by file_id")
    parser.add_argument("--view", type=str, help="Save specific image to view locally by file_id")
    
    args = parser.parse_args()
    
    if args.list:
        list_all_images()
    elif args.export:
        export_all_images()
    elif args.info:
        get_image_info(args.info)
    elif args.view:
        view_single_image(args.view)
    else:
        print("🖼️  Lost & Found Portal - Image Viewer Utility")
        print("=" * 50)
        print("Usage:")
        print("  python view_images.py --list              # List all images")
        print("  python view_images.py --export            # Export all images")
        print("  python view_images.py --info <file_id>    # Image information")
        print("  python view_images.py --view <file_id>    # Save image to view")
        print("\nExample:")
        print("  python view_images.py --list")

if __name__ == "__main__":
    main()
