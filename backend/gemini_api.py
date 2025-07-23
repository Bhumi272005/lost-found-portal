

import google.generativeai as genai
from PIL import Image
import os

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
        
        # Open and process the image
        image = Image.open(path)
        
        # Generate content with the image and prompt
        response = model.generate_content([
            image, 
            "What object is in this image? Respond with a one-word category."
        ])
        
        return response.text.strip()
        
    except FileNotFoundError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Test function
if __name__ == "__main__":
    # Example usage
    image_path = "test_image.jpg"  # Replace with actual image path
    result = classify_image(image_path)
    print(f"Classification result: {result}")