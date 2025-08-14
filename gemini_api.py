

import google.generativeai as genai
from PIL import Image
import os
import requests
from io import BytesIO

# Configure with your actual API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: Please set your GEMINI_API_KEY environment variable")
    print("You can create a .env file with: GEMINI_API_KEY=your_actual_key")
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    # Use a placeholder key for testing (will cause API calls to fail but won't crash the app)
    api_key = "placeholder_key"

genai.configure(api_key=api_key)

def classify_image(path: str) -> str:
    try:
        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image file not found: {path}")
        
        # Use gemini-1.5-flash model (updated model name)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Open and process the image with proper context management
        with Image.open(path) as image:
            # Generate content with the image and prompt
            response = model.generate_content([
                image, 
                "What object is in this image? Respond with a one-word category."
            ])
        
        return response.text.strip()
        
    except FileNotFoundError as e:
        print(f"Gemini API: File not found - {str(e)}")
        return "Uncategorized"
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return "Uncategorized"

def classify_image_from_url(image_url: str) -> str:
    """Classify image from URL using Gemini API - for shareable URLs"""
    try:
        # Check if URL is provided
        if not image_url:
            raise ValueError("No image URL provided")
        
        print(f"Downloading image from URL: {image_url}")
        
        # Download image from URL
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Convert to PIL Image
        image = Image.open(BytesIO(response.content))
        
        # Use gemini-1.5-flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content with the image and prompt
        ai_response = model.generate_content([
            image, 
            "What object is in this image? Respond with a one-word category like: phone, wallet, keys, bag, book, electronics, clothing, jewelry, documents, etc."
        ])
        
        return ai_response.text.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Gemini API: Error downloading image from URL - {str(e)}")
        return "Uncategorized"
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return "Uncategorized"

def classify_image_from_bytes(image_data: bytes) -> str:
    """Classify image from bytes data using Gemini API"""
    try:
        # Check if image data is provided
        if not image_data:
            raise ValueError("No image data provided")
        
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(image_data))
        
        # Use gemini-1.5-flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content with the image and prompt
        response = model.generate_content([
            image, 
            "What object is in this image? Respond with a one-word category like: phone, wallet, keys, bag, book, electronics, clothing, jewelry, documents, etc."
        ])
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return "Uncategorized"

def search_similar_items_by_category(query_category: str, items_with_urls: list) -> list:
    """Search for similar items using category matching"""
    try:
        similar_items = []
        query_lower = query_category.lower()
        
        for item in items_with_urls:
            # Check multiple fields for category matches
            category_match = (
                (item.get('category') and query_lower in item['category'].lower()) or
                (item.get('ai_category') and query_lower in item['ai_category'].lower()) or
                (item.get('title') and query_lower in item['title'].lower()) or
                (item.get('description') and query_lower in item['description'].lower())
            )
            
            if category_match:
                similar_items.append(item)
        
        return similar_items
        
    except Exception as e:
        print(f"Error in similarity search: {str(e)}")
        return []

# Test function
if __name__ == "__main__":
    # Example usage with file path
    image_path = "test_image.jpg"  # Replace with actual image path
    result = classify_image(image_path)
    print(f"Classification result from file: {result}")
    
    # Example usage with URL
    test_url = "http://localhost:8000/images/YOUR_FILE_ID"  # Replace with actual URL
    url_result = classify_image_from_url(test_url)
    print(f"Classification result from URL: {url_result}")
    
    # Example with bytes (for testing)
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        bytes_result = classify_image_from_bytes(image_bytes)
        print(f"Classification result from bytes: {bytes_result}")
    except FileNotFoundError:
        print("Test image file not found for bytes test")