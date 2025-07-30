"""
Demonstration: How to use shareable URLs for images with Gemini AI
"""
import requests
from backend.gemini_api import classify_image_from_url
from backend.mongodb import search_by_image_url, fetch_all_items_with_urls

def demo_shareable_urls():
    """Demonstrate how shareable URLs work"""
    print("🌟 SHAREABLE URLS DEMONSTRATION")
    print("=" * 60)
    
    # Get your network IP
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        network_ip = s.getsockname()[0]
        s.close()
    except:
        network_ip = "192.168.0.101"  # Your detected IP
    
    print(f"🌐 Your Network IP: {network_ip}")
    print(f"🔗 Base URL: http://{network_ip}:8000")
    
    # Get items from database
    items = fetch_all_items_with_urls()
    
    if not items:
        print("❌ No items found in database")
        return
    
    print(f"\n📦 Found {len(items)} items with images:")
    
    for i, item in enumerate(items):
        print(f"\n--- Item {i+1}: {item['title']} ---")
        print(f"📝 Description: {item['description']}")
        print(f"📂 Category: {item['category']}")
        print(f"🤖 AI Category: {item.get('ai_category', 'Not classified')}")
        
        if item.get('image_file_id'):
            # Show different URL formats
            localhost_url = f"http://localhost:8000/images/{item['image_file_id']}"
            network_url = f"http://{network_ip}:8000/images/{item['image_file_id']}"
            
            print(f"🔗 Local URL: {localhost_url}")
            print(f"🌐 Network URL: {network_url}")
            print("   ^ Share this URL with other computers!")
            
            # Test Gemini AI classification
            print("\n🤖 Testing Gemini AI classification...")
            try:
                ai_result = classify_image_from_url(localhost_url)
                print(f"✅ AI Classification: {ai_result}")
            except Exception as e:
                print(f"❌ AI Classification failed: {e}")
            
            # Test search by image
            print("\n🔍 Testing search by similar images...")
            try:
                similar_items = search_by_image_url(localhost_url)
                print(f"✅ Found {len(similar_items)} similar items")
                
                for sim_item in similar_items[:2]:  # Show first 2
                    print(f"   📦 {sim_item['title']} - {sim_item.get('ai_category', 'N/A')}")
                    
            except Exception as e:
                print(f"❌ Image search failed: {e}")
        else:
            print("❌ No image available")
        
        print("-" * 50)

def demo_api_endpoints():
    """Demonstrate API endpoints for shareable URLs"""
    print("\n🔌 API ENDPOINTS DEMONSTRATION")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    print("Available API endpoints:")
    print(f"1. Get all items with URLs: GET {base_url}/api/items-with-urls")
    print(f"2. Classify image: GET {base_url}/api/classify-image?image_url=YOUR_URL")
    print(f"3. Search by image: POST {base_url}/api/search-by-image-url")
    
    # Test API endpoints
    try:
        print("\n🧪 Testing API endpoints...")
        
        # Test get items with URLs
        response = requests.get(f"{base_url}/api/items-with-urls")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Items API: Found {data['count']} items")
            
            if data['items']:
                first_item = data['items'][0]
                if first_item.get('image_file_id'):
                    image_url = f"{base_url}/images/{first_item['image_file_id']}"
                    
                    # Test classify image API
                    classify_response = requests.get(
                        f"{base_url}/api/classify-image",
                        params={"image_url": image_url}
                    )
                    
                    if classify_response.status_code == 200:
                        classify_data = classify_response.json()
                        print(f"✅ Classify API: {classify_data['category']}")
                    else:
                        print(f"❌ Classify API failed: {classify_response.status_code}")
                    
                    # Test search by image API
                    search_response = requests.post(
                        f"{base_url}/api/search-by-image-url",
                        json={"image_url": image_url}
                    )
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        print(f"✅ Search API: Found {search_data['count']} results")
                    else:
                        print(f"❌ Search API failed: {search_response.status_code}")
                        
        else:
            print(f"❌ Items API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ API server not running. Start with: python backend/main.py")
    except Exception as e:
        print(f"❌ API test error: {e}")

def show_usage_examples():
    """Show practical usage examples"""
    print("\n📚 USAGE EXAMPLES")
    print("=" * 60)
    
    print("1. 🖥️ From Python code:")
    print("""
from backend.gemini_api import classify_image_from_url
from backend.mongodb import search_by_image_url

# Classify an image
url = "http://192.168.0.101:8000/images/6887a05b391f0148f06e9fdc"
category = classify_image_from_url(url)
print(f"Category: {category}")

# Search for similar items
results = search_by_image_url(url)
print(f"Found {len(results)} similar items")
""")
    
    print("2. 🌐 Share URLs with other computers:")
    print("""
# Replace 'localhost' with your IP address:
http://192.168.0.101:8000/images/6887a05b391f0148f06e9fdc

# Other computers can:
- View the image in browser
- Use it with AI classification
- Search for similar items
""")
    
    print("3. 📱 Via API calls (from any programming language):")
    print("""
# Classify image
GET http://192.168.0.101:8000/api/classify-image?image_url=YOUR_URL

# Search similar items
POST http://192.168.0.101:8000/api/search-by-image-url
Body: {"image_url": "YOUR_URL"}
""")

if __name__ == "__main__":
    demo_shareable_urls()
    demo_api_endpoints()
    show_usage_examples()
    
    print("\n🎉 SUMMARY")
    print("=" * 60)
    print("✅ Images are stored in MongoDB GridFS")
    print("✅ Each image has a shareable URL")
    print("✅ URLs work across different computers")
    print("✅ Gemini AI can classify images from URLs")
    print("✅ Search functionality works with URLs")
    print("✅ API endpoints available for integration")
    
    print("\n💡 Next steps:")
    print("1. Set your GEMINI_API_KEY in .env file")
    print("2. Update BASE_URL to your network IP")
    print("3. Share URLs with other computers")
    print("4. Test AI classification and search!")
