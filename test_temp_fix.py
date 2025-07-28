"""
Test script to verify the temporary file handling fix
"""
import requests
import os
from PIL import Image
import io

def create_test_image():
    """Create a simple test image"""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

def test_report_item():
    """Test reporting an item to check if temporary file error is fixed"""
    print("🧪 Testing item report with image upload...")
    
    # Create test image
    image_data = create_test_image()
    
    # Prepare form data
    data = {
        'title': 'Test Item',
        'description': 'Test description to verify temp file fix',
        'location': 'Test Location',
        'status': 'Lost',
        'name': 'Test User',
        'contact': 'test@example.com'
    }
    
    # Prepare file
    files = {
        'file': ('test_image.jpg', image_data, 'image/jpeg')
    }
    
    try:
        # Make request to report endpoint
        response = requests.post('http://localhost:8000/report/', data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Item reported successfully")
            print(f"   Category detected: {result.get('category', 'N/A')}")
            print(f"   Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_temp_files():
    """Check if any temporary files remain"""
    print("\n🔍 Checking for remaining temporary files...")
    temp_files = [f for f in os.listdir('.') if f.startswith('temp_') and f.endswith('.jpg')]
    
    if temp_files:
        print(f"⚠️ Found {len(temp_files)} temporary files:")
        for f in temp_files:
            print(f"   - {f}")
        return False
    else:
        print("✅ No temporary files found - cleanup working correctly!")
        return True

if __name__ == "__main__":
    print("🚀 Lost & Found API - Temporary File Fix Test")
    print("=" * 50)
    
    # Test the API
    success = test_report_item()
    
    # Check for temp files
    no_temp_files = check_temp_files()
    
    print("\n📊 Test Results:")
    print(f"   API Request: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"   Temp File Cleanup: {'✅ PASS' if no_temp_files else '❌ FAIL'}")
    
    if success and no_temp_files:
        print("\n🎉 All tests passed! The temporary file issue has been fixed.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
