"""
Test script for shareable URLs and Gemini API integration
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_image_url_classification():
    """Test classifying images from URLs"""
    print("🧪 Testing Image URL Classification")
    print("=" * 50)
    
    # Import after adding to path
    from backend.gemini_api import classify_image_from_url
    
    # Test URLs (replace with actual URLs from your database)
    test_urls = [
        "http://localhost:8000/images/YOUR_FILE_ID_1",  # Replace with real file ID
        "http://localhost:8000/images/YOUR_FILE_ID_2",  # Replace with real file ID
    ]
    
    for url in test_urls:
        try:
            print(f"Testing URL: {url}")
            category = classify_image_from_url(url)
            print(f"✅ Category: {category}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 30)

def test_database_connection():
    """Test MongoDB connection and fetch items with URLs"""
    print("\n🔗 Testing Database Connection")
    print("=" * 50)
    
    try:
        from backend.mongodb import fetch_all_items_with_urls, get_mongodb
        
        # Test connection
        mongodb = get_mongodb()
        print("✅ MongoDB connected successfully")
        
        # Fetch items with URLs
        items = fetch_all_items_with_urls()
        print(f"📊 Found {len(items)} items in database")
        
        # Display first few items with URLs
        for i, item in enumerate(items[:3]):  # Show first 3 items
            print(f"\n📦 Item {i+1}:")
            print(f"   Title: {item['title']}")
            print(f"   Category: {item['category']}")
            print(f"   AI Category: {item.get('ai_category', 'N/A')}")
            print(f"   Image URL: {item.get('image_url', 'No image')}")
            
    except Exception as e:
        print(f"❌ Database error: {e}")

def test_search_by_image():
    """Test searching similar items by image URL"""
    print("\n🔍 Testing Image-Based Search")
    print("=" * 50)
    
    try:
        from backend.mongodb import search_by_image_url
        
        # Replace with actual image URL from your database
        test_search_url = "http://localhost:8000/images/YOUR_FILE_ID"
        
        print(f"Searching for similar items using: {test_search_url}")
        results = search_by_image_url(test_search_url)
        
        print(f"🔍 Found {len(results)} similar items")
        
        for i, item in enumerate(results[:3]):  # Show first 3 results
            print(f"\n📦 Similar Item {i+1}:")
            print(f"   Title: {item['title']}")
            print(f"   Category: {item['category']}")
            print(f"   AI Category: {item.get('ai_category', 'N/A')}")
            print(f"   Image URL: {item.get('image_url', 'No image')}")
            
    except Exception as e:
        print(f"❌ Search error: {e}")

def show_shareable_urls_guide():
    """Show guide for using shareable URLs"""
    print("\n📋 Shareable URLs Guide")
    print("=" * 50)
    
    print("1. 🌐 Your images are accessible via URLs like:")
    print("   http://localhost:8000/images/{file_id}")
    print("   http://YOUR_IP:8000/images/{file_id}")
    
    print("\n2. 🖥️ For other computers to access:")
    print("   - Find your IP: ipconfig (Windows) or ifconfig (Mac/Linux)")
    print("   - Replace 'localhost' with your IP address")
    print("   - Example: http://192.168.1.100:8000/images/{file_id}")
    
    print("\n3. 🤖 Gemini AI can classify images from these URLs:")
    print("   - classify_image_from_url('http://YOUR_IP:8000/images/file_id')")
    
    print("\n4. 🔍 Search similar items:")
    print("   - search_by_image_url('http://YOUR_IP:8000/images/file_id')")
    
    print("\n5. 📱 Share URLs with anyone on the network!")

def get_network_ip():
    """Get the network IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    print("🚀 Lost & Found - Shareable URLs Test")
    print("=" * 60)
    
    # Show network info
    network_ip = get_network_ip()
    print(f"🌐 Your network IP: {network_ip}")
    print(f"🔗 Shareable base URL: http://{network_ip}:8000")
    
    # Run tests
    test_database_connection()
    show_shareable_urls_guide()
    
    # Uncomment these when you have actual URLs to test
    # test_image_url_classification()
    # test_search_by_image()
    
    print("\n✅ Test completed!")
    print("💡 Replace 'YOUR_FILE_ID' with actual file IDs from your database")
