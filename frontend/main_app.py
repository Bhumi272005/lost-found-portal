import streamlit as st
import requests
from PIL import Image
import io
import datetime
import pytz
import os

# Configuration for Streamlit deployment
st.set_page_config(
    page_title="Lost & Found Portal", 
    layout="centered", 
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

# Get API URL from environment or use default
# For local development, use localhost. For production, use Railway URL
try:
    # Try to get from Streamlit secrets first (for Streamlit Cloud deployment)
    API_URL = st.secrets.get("api", {}).get("API_URL", "")
    if not API_URL:
        # Fallback to environment variable
        API_URL = os.getenv("API_URL", "")
    if not API_URL:
        # Default for local development
        API_URL = "http://localhost:8000"
except:
    # Fallback if secrets not available
    API_URL = os.getenv("API_URL", "http://localhost:8000")

def get_image_url(image_file_id):
    """Convert GridFS file ID to API URL"""
    if not image_file_id:
        return None
    
    # Return the full URL to the image served by FastAPI from GridFS
    return f"{API_URL}/images/{image_file_id}"

def display_image(image_file_id, width=150):
    """Display image using GridFS file ID or show placeholder"""
    if image_file_id:
        try:
            image_url = get_image_url(image_file_id)
            st.image(image_url, width=width)
        except Exception as e:
            st.write("📷 Image not found")
    else:
        st.write("📷 No image")

# Check API connectivity
@st.cache_data(ttl=30)
def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# --- Main App ---
def main():
    st.title("🔍 Lost & Found Portal")
    st.markdown("Find and report lost items easily")
    
    # Show connection status
    with st.sidebar:
        st.write("🔗 **API Connection**")
        if "localhost" in API_URL:
            st.write(f"🏠 Local: `{API_URL}`")
        else:
            st.write(f"☁️ Cloud: `{API_URL}`")
        
        # Check API health
        if check_api_health():
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.write("Make sure your backend is running")
        
        st.write("---")
    
    # Navigation
    tab1, tab2, tab3 = st.tabs(["📋 View Items", "📝 Report Item", "🔍 Search"])
    
    with tab1:
        view_items()
    
    with tab2:
        report_item()
    
    with tab3:
        search_items()

def view_items():
    """Display all lost and found items"""
    st.header("📋 All Items")
    
    try:
        response = requests.get(f"{API_URL}/items/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                st.info("No items found. Be the first to report an item!")
                return
            
            st.write(f"Found {len(items)} items")
            
            for item in items:
                if len(item) >= 9:
                    item_id, title, description, category, location, status, name, contact, image_url, timestamp = item[:10]
                    
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            if image_url:
                                display_image(image_url.split('/')[-1] if '/images/' in image_url else image_url)
                            else:
                                st.write("📷 No image")
                        
                        with col2:
                            st.subheader(f"{title}")
                            st.write(f"**Status**: {status}")
                            st.write(f"**Category**: {category}")
                            st.write(f"**Location**: {location}")
                            if description:
                                st.write(f"**Description**: {description}")
                            st.write(f"**Contact**: {name} - {contact}")
                            st.write(f"**Posted**: {timestamp}")
                        
                        st.write("---")
        else:
            st.error(f"Failed to fetch items: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.write("Make sure your backend is running and accessible.")

def report_item():
    """Report a new lost or found item"""
    st.header("📝 Report an Item")
    
    with st.form("report_form"):
        title = st.text_input("Item Title*", placeholder="e.g., Blue wallet, iPhone 13, etc.")
        description = st.text_area("Description", placeholder="Detailed description of the item...")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", [
                "Electronics", "Clothing", "Accessories", "Documents", 
                "Books", "Sports Equipment", "Other"
            ])
            status = st.selectbox("Status*", ["Lost", "Found"])
        
        with col2:
            location = st.text_input("Location*", placeholder="Where was it lost/found?")
        
        st.write("**Contact Information**")
        col3, col4 = st.columns(2)
        with col3:
            name = st.text_input("Your Name", placeholder="Optional")
        with col4:
            contact = st.text_input("Contact (Phone/Email)*", placeholder="How to reach you")
        
        image_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            if not title or not location or not contact:
                st.error("Please fill in all required fields (marked with *)")
                return
            
            try:
                # Prepare form data
                form_data = {
                    "title": title,
                    "description": description,
                    "category": category,
                    "location": location,
                    "status": status,
                    "name": name or "Anonymous",
                    "contact": contact
                }
                
                files = {}
                if image_file:
                    files["file"] = (image_file.name, image_file.getvalue(), image_file.type)
                
                # Submit to API
                response = requests.post(f"{API_URL}/report/", data=form_data, files=files, timeout=30)
                
                if response.status_code == 200:
                    st.success("✅ Item reported successfully!")
                    st.balloons()
                    st.write("Your item has been added to the database.")
                else:
                    st.error(f"Failed to submit: {response.status_code}")
                    st.write(response.text)
            
            except Exception as e:
                st.error(f"Error submitting report: {e}")

def search_items():
    """Search for items"""
    st.header("🔍 Search Items")
    
    search_query = st.text_input("Search for items", placeholder="Enter keywords...")
    status_filter = st.selectbox("Filter by status", ["All", "Lost", "Found"])
    
    if st.button("Search") or search_query:
        if not search_query:
            st.warning("Please enter a search query")
            return
        
        try:
            params = {"query": search_query}
            if status_filter != "All":
                params["status"] = status_filter
            
            response = requests.get(f"{API_URL}/search/", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                if not items:
                    st.info("No items found matching your search.")
                    return
                
                st.write(f"Found {len(items)} matching items")
                
                for item in items:
                    if len(item) >= 9:
                        item_id, title, description, category, location, status, name, contact, image_url, timestamp = item[:10]
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                if image_url:
                                    display_image(image_url.split('/')[-1] if '/images/' in image_url else image_url)
                                else:
                                    st.write("📷 No image")
                            
                            with col2:
                                st.subheader(f"{title}")
                                st.write(f"**Status**: {status}")
                                st.write(f"**Category**: {category}")
                                st.write(f"**Location**: {location}")
                                if description:
                                    st.write(f"**Description**: {description}")
                                st.write(f"**Contact**: {name} - {contact}")
                                st.write(f"**Posted**: {timestamp}")
                            
                            st.write("---")
            else:
                st.error(f"Search failed: {response.status_code}")
        
        except Exception as e:
            st.error(f"Error searching: {e}")

if __name__ == "__main__":
    main()
