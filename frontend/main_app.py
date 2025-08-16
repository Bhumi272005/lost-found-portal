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
    # Try multiple ways to get the API URL from Streamlit secrets
    API_URL = ""
    
    # Method 1: Nested format [api] section
    try:
        API_URL = st.secrets.get("api", {}).get("API_URL", "")
    except:
        pass
    
    # Method 2: Flat format (direct key)
    if not API_URL:
        try:
            API_URL = st.secrets.get("API_URL", "")
        except:
            pass
    
    # Method 3: Environment variable fallback
    if not API_URL:
        API_URL = os.getenv("API_URL", "")
    
    # Method 4: Default for local development
    if not API_URL:
        API_URL = "http://localhost:8000"
        
except Exception as e:
    # Final fallback if secrets not available
    API_URL = "http://localhost:8000"

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
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Lost & Found Portal</h1>
        <p>Connecting students with their lost belongings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation with clean page selection
    page_options = ["🔍 Search Items", "📝 Report Item"]
    
    page = st.selectbox(
        "Navigate to:",
        page_options,
        label_visibility="collapsed"
    )
    
    # Route to appropriate page
    if page == "🔍 Search Items":
        search_page()
    elif page == "📝 Report Item":
        report_page()

def search_page():
    """Enhanced search page with semantic search"""
    st.markdown("""
    <div class="search-container">
        <p>Find your lost items or help others by searching our database</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search form
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search for items", 
            placeholder="e.g., 'blue wallet', 'iPhone', 'textbook', 'keys'...",
            label_visibility="collapsed"
        )
    with col2:
        status_filter = st.selectbox("Filter", ["All Items", "Lost", "Found"])
    
    # Search button
    if st.button("Search", type="primary", use_container_width=True) or search_query:
        if search_query:
            search_results(search_query, status_filter)
        else:
            st.warning("Please enter a search term")
    
    # Display all items if no search
    if not search_query:
        st.subheader("Recent Items")
        display_all_items()

def search_results(query, status_filter):
    """Display search results"""
    try:
        params = {"q": query}  # Changed from "query" to "q" to match backend
        if status_filter != "All Items":
            params["status"] = status_filter
        
        response = requests.get(f"{API_URL}/search/", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                st.info("No items found matching your search. Try different keywords.")
                return
            
            st.success(f"Found {len(items)} matching items")
            
            for item in items:
                display_item_card(item)
        else:
            st.error("Search service temporarily unavailable. Please try again.")
    
    except Exception as e:
        st.error("Unable to connect to search service. Please check your connection.")

def display_all_items():
    """Display all items in a clean format"""
    try:
        response = requests.get(f"{API_URL}/items/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                st.info("No items reported yet. Be the first to report an item!")
                return
            
            # Show recent items (limit to 10 for performance)
            recent_items = items[:10] if len(items) > 10 else items
            
            for item in recent_items:
                display_item_card(item)
            
            if len(items) > 10:
                st.info(f"Showing 10 most recent items. Total items: {len(items)}")
        else:
            st.error("Unable to load items")
    
    except Exception as e:
        st.error("Service temporarily unavailable")

def display_item_card(item):
    """Display individual item in a professional card format"""
    if len(item) >= 9:
        item_id, title, description, category, location, status, name, contact, image_url, timestamp = item[:10]
        
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if image_url:
                try:
                    image_id = image_url.split('/')[-1] if '/images/' in image_url else image_url
                    st.image(f"{API_URL}/images/{image_id}", width=120)
                except:
                    st.write("📷")
            else:
                st.write("📷")
        
        with col2:
            st.markdown(f"**{title}**")
            
            # Status badge
            if status == "Lost":
                st.markdown('<span class="status-badge status-lost">Lost Item</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-badge status-found">Found Item</span>', unsafe_allow_html=True)
            
            st.write(f"**Location:** {location}")
            st.write(f"**Category:** {category}")
            if description:
                st.write(f"**Details:** {description}")
        
        with col3:
            st.write(f"**Contact:**")
            st.write(f"{name}")
            st.write(f"{contact}")
            st.caption(f"Posted: {timestamp[:10]}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def report_page():
    """Professional report page"""
    st.markdown("""
    <div class="search-container">
        <p>Help your fellow students by reporting lost or found items</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("professional_report_form", clear_on_submit=True):
        st.subheader("Item Information")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Item Name *", placeholder="e.g., Blue Wallet, iPhone 13, Physics Textbook")
            category = st.selectbox("Category", [
                "Electronics", "Books & Stationery", "Clothing & Accessories", 
                "Documents & Cards", "Sports Equipment", "Personal Items", "Other"
            ])
        
        with col2:
            status = st.selectbox("Status *", ["Lost", "Found"])
            location = st.text_input("Location *", placeholder="e.g., Library, Cafeteria, Main Building")
        
        description = st.text_area(
            "Description", 
            placeholder="Provide detailed description including color, brand, size, distinctive features...",
            height=100
        )
        
        st.subheader("Contact Information")
        col3, col4 = st.columns(2)
        with col3:
            name = st.text_input("Your Name", placeholder="Anonymous (optional)")
        with col4:
            contact = st.text_input("Contact Information *", placeholder="Phone number or email")
        
        st.subheader("Upload Image *")
        image_file = st.file_uploader(
            "Choose an image file *", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of the item (required for identification)"
        )
        
        # Submit button
        col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
        with col_submit2:
            submitted = st.form_submit_button("Submit Report", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not title.strip():
                st.error("Please enter the item name")
                return
            if not location.strip():
                st.error("Please specify the location")
                return
            if not contact.strip():
                st.error("Contact information is required")
                return
            if not image_file:
                st.error("Please upload an image of the item")
                return
            
            # Submit to API
            try:
                with st.spinner("Submitting your report..."):
                    form_data = {
                        "title": title.strip(),
                        "description": description.strip() if description else "",
                        "category": category,
                        "location": location.strip(),
                        "status": status,
                        "name": name.strip() if name.strip() else "Anonymous",
                        "contact": contact.strip()
                    }
                    
                    files = {}
                    if image_file:
                        files["file"] = (image_file.name, image_file.getvalue(), image_file.type)
                    
                    response = requests.post(f"{API_URL}/report/", data=form_data, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        st.success("✅ Report submitted successfully!")
                    else:
                        st.error("Failed to submit report. Please try again.")
                        
            except Exception as e:
                st.error("Unable to submit report. Please check your connection and try again.")



if __name__ == "__main__":
    main()
