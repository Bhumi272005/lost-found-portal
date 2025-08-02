<<<<<<< HEAD
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
# For Streamlit Cloud deployment, you'll need to set this in your secrets
API_URL = st.secrets.get("API_URL", "https://your-backend-api.herokuapp.com")

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

# --- Sidebar for Navigation ---
st.sidebar.title("Lost & Found Portal")

# API Health Check
if check_api_health():
    st.sidebar.success("API Connected")
else:
    st.sidebar.error("API Disconnected")
    st.error("⚠️ Cannot connect to backend server. Please check your API URL configuration.")

# Check if user is admin
is_admin = st.session_state.get("admin_authenticated", False)

# Navigation options based on user role
if is_admin:
    page = st.sidebar.radio("📁Navigate", ["🔍 Search Items", "📝 Report Item", "⚙️ Admin Panel"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Admin Logout"):
        st.session_state.admin_authenticated = False
        st.success("✅ Logged out successfully!")
        st.rerun()
else:
    page = st.sidebar.radio("📁 Navigate", ["🔍 Search Items", "📝 Report Item"])
    st.sidebar.markdown("---")
    if st.sidebar.button("🔐 Admin Login"):
        st.session_state.show_admin_login = True

# Handle admin login from sidebar
if st.session_state.get("show_admin_login", False):
    st.title("🔐 Admin Login")
    
    admin_password = st.text_input("Enter Admin Password:", type="password", key="sidebar_admin_pwd")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login", key="sidebar_login"):
            # Get admin password from secrets or use default
            correct_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
            if admin_password == correct_password:
                st.session_state.admin_authenticated = True
                st.session_state.show_admin_login = False
                st.success("✅ Authentication successful! Welcome Admin!")
                st.rerun()
            else:
                st.error("❌ Invalid password!")
    
    with col2:
        if st.button("🚫 Cancel", key="sidebar_cancel"):
            st.session_state.show_admin_login = False
            st.rerun()
    
    st.stop()

# --- Page 1: Search Items ---
if page == "🔍 Search Items":
    st.title("🔍 Search Lost/Found Items")

    search_text = st.text_input("Enter item description (or type of item):", "")
    status_filter = st.selectbox("Filter by status:", ["All", "Lost", "Found"])

    st.markdown("Or upload an image to search by visual similarity:")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("🔍 Search"):
        if search_text.strip():
            st.info(f"Searching for: '{search_text}'")
            try:
                search_response = requests.get(f"{API_URL}/search/", params={"q": search_text, "status": status_filter})
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    search_items = search_data.get("items", [])
                    st.success(f"🎯 Found {len(search_items)} matching items")
                    
                    # Display search results
                    for item in search_items:
                        id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                display_image(img_file_id)
                            with col2:
                                st.markdown(f"**{title}** ({status})")
                                st.markdown(f"**Description:** {desc}")
                                st.markdown(f"**Location:** {loc}")
                                st.markdown(f"**Reported by:** {name}")
                                st.markdown(f"**Contact:** `{contact}`")
                                st.markdown(f"**Date:** {timestamp}")
                        st.markdown("---")
                else:
                    st.error("❌ Search failed")
            except Exception as e:
                st.error(f"❌ Search error: {e}")
        elif uploaded_image:
            st.info("Searching for visually similar items...")
            try:
                files = {"file": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)}
                visual_response = requests.post(f"{API_URL}/search/visual/", files=files)
                
                if visual_response.status_code == 200:
                    visual_data = visual_response.json()
                    visual_items = visual_data.get("items", [])
                    st.success(f"🎯 Found {len(visual_items)} visually similar items")
                    
                    # Display visual search results
                    for item in visual_items:
                        if len(item) > 10:  # Has similarity score
                            id, title, desc, category, loc, status, name, contact, img_file_id, timestamp, similarity = item
                            similarity_percent = round(similarity * 100, 1)
                        else:
                            id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                            similarity_percent = 0
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                display_image(img_file_id)
                            with col2:
                                st.markdown(f"**{title}** ({status})")
                                st.markdown(f"**Similarity:** {similarity_percent}%")
                                st.markdown(f"**Description:** {desc}")
                                st.markdown(f"**Location:** {loc}")
                                st.markdown(f"**Reported by:** {name}")
                                st.markdown(f"**Contact:** `{contact}`")
                                st.markdown(f"**Date:** {timestamp}")
                        st.markdown("---")
                else:
                    st.error("❌ Visual search failed")
            except Exception as e:
                st.error(f"❌ Visual search error: {e}")
        else:
            st.warning("⚠️ Please enter a search term or upload an image")

    st.markdown("---")
    st.subheader("🗃️ Recently Reported Items")

    try:
        response = requests.get(f"{API_URL}/items/")
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            if items:
                for item in items:
                    id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                    if status_filter != "All" and status != status_filter:
                        continue

                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            display_image(img_file_id)
                        with col2:
                            st.markdown(f"**{title}** ({status})")
                            st.markdown(f"**Description:** {desc}")
                            st.markdown(f"**Location:** {loc}")
                            st.markdown(f"**Reported by:** {name}")
                            st.markdown(f"**Contact:** `{contact}`")
                            st.markdown(f"**Date:** {timestamp}")
                    st.markdown("---")
            else:
                st.info("📭 No items reported yet. Be the first to report a lost or found item!")
        else:
            st.warning("Could not load items from the server.")

    except Exception as e:
        st.error(f"Error fetching items: {e}")

# --- Page 2: Report Lost/Found Item ---
elif page == "📝 Report Item":
    st.title("📝 Report a Lost or Found Item")

    col1, col2 = st.columns([2, 1])
    with col1:
        status = st.radio("Item Type", ["Lost", "Found"])
        title = st.text_input("Item Title")
        description = st.text_area("Item Description")
        location = st.text_input("Last Seen / Found Location")
    
    with col2:
        name = st.text_input("Your Name (Optional)", value="Anonymous")
        contact = st.text_input("Your Contact (Required)")

    st.markdown("**📷 Upload Item Image:**")
    camera_image = st.camera_input("Take a picture")
    file_image = st.file_uploader("Or upload from gallery", type=["jpg", "jpeg", "png"])

    image_file = camera_image or file_image

    if st.button("Submit Report", type="primary"):
        if not contact:
            st.warning("⚠️ Contact is mandatory.")
        elif not image_file:
            st.warning("⚠️ Please upload or capture an image.")
        elif not title:
            st.warning("⚠️ Please provide an item title.")
        else:
            with st.spinner("Uploading..."):
                files = {"file": (image_file.name, image_file.getvalue(), "image/jpeg")}
                data = {
                    "title": title,
                    "description": description,
                    "location": location,
                    "status": status,
                    "name": name,
                    "contact": contact,
                }
                try:
                    response = requests.post(f"{API_URL}/report/", data=data, files=files)
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Report submitted successfully!")
                        if result.get("category"):
                            st.info(f"🏷️ Auto-detected category: **{result['category']}**")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Failed to connect to backend: {e}")

# --- Page 3: Admin Panel ---
elif page == "⚙️ Admin Panel":
    st.title("⚙️ Admin Dashboard")
    
    if not st.session_state.get("admin_authenticated", False):
        st.error("🚫 Access Denied: Admin authentication required")
        st.stop()
    
    # Display all items with delete functionality
    try:
        response = requests.get(f"{API_URL}/items/")
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            # Admin statistics
            lost_items = [item for item in items if item[5] == "Lost"]
            found_items = [item for item in items if item[5] == "Found"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Items", len(items))
            with col2:
                st.metric("Lost Items", len(lost_items))
            with col3:
                st.metric("Found Items", len(found_items))
            
            st.markdown("---")
            
            if items:
                st.subheader("🗂️ All Items Management")
                for item in items:
                    id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                    
                    status_icon = "❌" if status == "Lost" else "✅"
                    
                    with st.expander(f"{status_icon} {title} ({status}) - ID: {id}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            if img_file_id:
                                try:
                                    image_url = get_image_url(img_file_id)
                                    st.image(image_url, width=200, caption=f"Item: {title}")
                                except:
                                    st.info("📷 Image not accessible")
                            else:
                                st.info("📷 No image available")
                            
                            st.markdown(f"**Description:** {desc}")
                            st.markdown(f"**Location:** {loc}")
                            st.markdown(f"**Reported by:** {name}")
                            st.markdown(f"**Contact:** `{contact}`")
                            st.markdown(f"**Timestamp:** {timestamp}")
                            st.markdown(f"**Category:** {category}")
                        
                        with col2:
                            st.markdown("**⚙️ Actions**")
                            if st.button(f"Delete Item", key=f"delete_{id}", type="secondary"):
                                st.session_state[f"confirm_delete_{id}"] = True
                            
                            if st.session_state.get(f"confirm_delete_{id}", False):
                                st.warning("⚠️ Are you sure?")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("Yes", key=f"confirm_yes_{id}"):
                                        try:
                                            del_response = requests.delete(f"{API_URL}/items/{id}")
                                            if del_response.status_code == 200:
                                                st.success(f"✅ Item deleted!")
                                                if f"confirm_delete_{id}" in st.session_state:
                                                    del st.session_state[f"confirm_delete_{id}"]
                                                st.rerun()
                                            else:
                                                st.error(f"Error: {del_response.text}")
                                        except Exception as e:
                                            st.error(f"Failed to delete: {e}")
                                with col_no:
                                    if st.button("No", key=f"confirm_no_{id}"):
                                        if f"confirm_delete_{id}" in st.session_state:
                                            del st.session_state[f"confirm_delete_{id}"]
                                        st.rerun()
            else:
                st.info("📭 No items found in the database.")
                st.markdown("*Items will appear here once users start reporting lost/found items.*")
        else:
            st.error("Could not connect to the backend API.")
            
    except Exception as e:
        st.error(f"Error fetching items: {e}")
        st.info("Make sure the backend API server is running.")

# Footer
st.markdown("---")
st.markdown("*Lost & Found Portal - Connecting people with their belongings*")
=======
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
# For Streamlit Cloud deployment, you'll need to set this in your secrets
API_URL = st.secrets.get("API_URL", "https://your-backend-api.herokuapp.com")

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

# --- Sidebar for Navigation ---
st.sidebar.title("Lost & Found Portal")

# API Health Check
if check_api_health():
    st.sidebar.success("API Connected")
else:
    st.sidebar.error("API Disconnected")
    st.error("⚠️ Cannot connect to backend server. Please check your API URL configuration.")

# Check if user is admin
is_admin = st.session_state.get("admin_authenticated", False)

# Navigation options based on user role
if is_admin:
    page = st.sidebar.radio("📁Navigate", ["🔍 Search Items", "📝 Report Item", "⚙️ Admin Panel"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Admin Logout"):
        st.session_state.admin_authenticated = False
        st.success("✅ Logged out successfully!")
        st.rerun()
else:
    page = st.sidebar.radio("📁 Navigate", ["🔍 Search Items", "📝 Report Item"])
    st.sidebar.markdown("---")
    if st.sidebar.button("🔐 Admin Login"):
        st.session_state.show_admin_login = True

# Handle admin login from sidebar
if st.session_state.get("show_admin_login", False):
    st.title("🔐 Admin Login")
    
    admin_password = st.text_input("Enter Admin Password:", type="password", key="sidebar_admin_pwd")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login", key="sidebar_login"):
            # Get admin password from secrets or use default
            correct_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
            if admin_password == correct_password:
                st.session_state.admin_authenticated = True
                st.session_state.show_admin_login = False
                st.success("✅ Authentication successful! Welcome Admin!")
                st.rerun()
            else:
                st.error("❌ Invalid password!")
    
    with col2:
        if st.button("🚫 Cancel", key="sidebar_cancel"):
            st.session_state.show_admin_login = False
            st.rerun()
    
    st.stop()

# --- Page 1: Search Items ---
if page == "🔍 Search Items":
    st.title("🔍 Search Lost/Found Items")

    search_text = st.text_input("Enter item description (or type of item):", "")
    status_filter = st.selectbox("Filter by status:", ["All", "Lost", "Found"])

    st.markdown("Or upload an image to search by visual similarity:")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("🔍 Search"):
        if search_text.strip():
            st.info(f"Searching for: '{search_text}'")
            try:
                search_response = requests.get(f"{API_URL}/search/", params={"q": search_text, "status": status_filter})
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    search_items = search_data.get("items", [])
                    st.success(f"🎯 Found {len(search_items)} matching items")
                    
                    # Display search results
                    for item in search_items:
                        id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                display_image(img_file_id)
                            with col2:
                                st.markdown(f"**{title}** ({status})")
                                st.markdown(f"**Description:** {desc}")
                                st.markdown(f"**Location:** {loc}")
                                st.markdown(f"**Reported by:** {name}")
                                st.markdown(f"**Contact:** `{contact}`")
                                st.markdown(f"**Date:** {timestamp}")
                        st.markdown("---")
                else:
                    st.error("❌ Search failed")
            except Exception as e:
                st.error(f"❌ Search error: {e}")
        elif uploaded_image:
            st.info("Searching for visually similar items...")
            try:
                files = {"file": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)}
                visual_response = requests.post(f"{API_URL}/search/visual/", files=files)
                
                if visual_response.status_code == 200:
                    visual_data = visual_response.json()
                    visual_items = visual_data.get("items", [])
                    st.success(f"🎯 Found {len(visual_items)} visually similar items")
                    
                    # Display visual search results
                    for item in visual_items:
                        if len(item) > 10:  # Has similarity score
                            id, title, desc, category, loc, status, name, contact, img_file_id, timestamp, similarity = item
                            similarity_percent = round(similarity * 100, 1)
                        else:
                            id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                            similarity_percent = 0
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                display_image(img_file_id)
                            with col2:
                                st.markdown(f"**{title}** ({status})")
                                st.markdown(f"**Similarity:** {similarity_percent}%")
                                st.markdown(f"**Description:** {desc}")
                                st.markdown(f"**Location:** {loc}")
                                st.markdown(f"**Reported by:** {name}")
                                st.markdown(f"**Contact:** `{contact}`")
                                st.markdown(f"**Date:** {timestamp}")
                        st.markdown("---")
                else:
                    st.error("❌ Visual search failed")
            except Exception as e:
                st.error(f"❌ Visual search error: {e}")
        else:
            st.warning("⚠️ Please enter a search term or upload an image")

    st.markdown("---")
    st.subheader("🗃️ Recently Reported Items")

    try:
        response = requests.get(f"{API_URL}/items/")
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            if items:
                for item in items:
                    id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                    if status_filter != "All" and status != status_filter:
                        continue

                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            display_image(img_file_id)
                        with col2:
                            st.markdown(f"**{title}** ({status})")
                            st.markdown(f"**Description:** {desc}")
                            st.markdown(f"**Location:** {loc}")
                            st.markdown(f"**Reported by:** {name}")
                            st.markdown(f"**Contact:** `{contact}`")
                            st.markdown(f"**Date:** {timestamp}")
                    st.markdown("---")
            else:
                st.info("📭 No items reported yet. Be the first to report a lost or found item!")
        else:
            st.warning("Could not load items from the server.")

    except Exception as e:
        st.error(f"Error fetching items: {e}")

# --- Page 2: Report Lost/Found Item ---
elif page == "📝 Report Item":
    st.title("📝 Report a Lost or Found Item")

    col1, col2 = st.columns([2, 1])
    with col1:
        status = st.radio("Item Type", ["Lost", "Found"])
        title = st.text_input("Item Title")
        description = st.text_area("Item Description")
        location = st.text_input("Last Seen / Found Location")
    
    with col2:
        name = st.text_input("Your Name (Optional)", value="Anonymous")
        contact = st.text_input("Your Contact (Required)")

    st.markdown("**📷 Upload Item Image:**")
    camera_image = st.camera_input("Take a picture")
    file_image = st.file_uploader("Or upload from gallery", type=["jpg", "jpeg", "png"])

    image_file = camera_image or file_image

    if st.button("Submit Report", type="primary"):
        if not contact:
            st.warning("⚠️ Contact is mandatory.")
        elif not image_file:
            st.warning("⚠️ Please upload or capture an image.")
        elif not title:
            st.warning("⚠️ Please provide an item title.")
        else:
            with st.spinner("Uploading..."):
                files = {"file": (image_file.name, image_file.getvalue(), "image/jpeg")}
                data = {
                    "title": title,
                    "description": description,
                    "location": location,
                    "status": status,
                    "name": name,
                    "contact": contact,
                }
                try:
                    response = requests.post(f"{API_URL}/report/", data=data, files=files)
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Report submitted successfully!")
                        if result.get("category"):
                            st.info(f"🏷️ Auto-detected category: **{result['category']}**")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Failed to connect to backend: {e}")

# --- Page 3: Admin Panel ---
elif page == "⚙️ Admin Panel":
    st.title("⚙️ Admin Dashboard")
    
    if not st.session_state.get("admin_authenticated", False):
        st.error("🚫 Access Denied: Admin authentication required")
        st.stop()
    
    # Display all items with delete functionality
    try:
        response = requests.get(f"{API_URL}/items/")
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            # Admin statistics
            lost_items = [item for item in items if item[5] == "Lost"]
            found_items = [item for item in items if item[5] == "Found"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Items", len(items))
            with col2:
                st.metric("Lost Items", len(lost_items))
            with col3:
                st.metric("Found Items", len(found_items))
            
            st.markdown("---")
            
            if items:
                st.subheader("🗂️ All Items Management")
                for item in items:
                    id, title, desc, category, loc, status, name, contact, img_file_id, timestamp = item
                    
                    status_icon = "❌" if status == "Lost" else "✅"
                    
                    with st.expander(f"{status_icon} {title} ({status}) - ID: {id}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            if img_file_id:
                                try:
                                    image_url = get_image_url(img_file_id)
                                    st.image(image_url, width=200, caption=f"Item: {title}")
                                except:
                                    st.info("📷 Image not accessible")
                            else:
                                st.info("📷 No image available")
                            
                            st.markdown(f"**Description:** {desc}")
                            st.markdown(f"**Location:** {loc}")
                            st.markdown(f"**Reported by:** {name}")
                            st.markdown(f"**Contact:** `{contact}`")
                            st.markdown(f"**Timestamp:** {timestamp}")
                            st.markdown(f"**Category:** {category}")
                        
                        with col2:
                            st.markdown("**⚙️ Actions**")
                            if st.button(f"Delete Item", key=f"delete_{id}", type="secondary"):
                                st.session_state[f"confirm_delete_{id}"] = True
                            
                            if st.session_state.get(f"confirm_delete_{id}", False):
                                st.warning("⚠️ Are you sure?")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("Yes", key=f"confirm_yes_{id}"):
                                        try:
                                            del_response = requests.delete(f"{API_URL}/items/{id}")
                                            if del_response.status_code == 200:
                                                st.success(f"✅ Item deleted!")
                                                if f"confirm_delete_{id}" in st.session_state:
                                                    del st.session_state[f"confirm_delete_{id}"]
                                                st.rerun()
                                            else:
                                                st.error(f"Error: {del_response.text}")
                                        except Exception as e:
                                            st.error(f"Failed to delete: {e}")
                                with col_no:
                                    if st.button("No", key=f"confirm_no_{id}"):
                                        if f"confirm_delete_{id}" in st.session_state:
                                            del st.session_state[f"confirm_delete_{id}"]
                                        st.rerun()
            else:
                st.info("📭 No items found in the database.")
                st.markdown("*Items will appear here once users start reporting lost/found items.*")
        else:
            st.error("Could not connect to the backend API.")
            
    except Exception as e:
        st.error(f"Error fetching items: {e}")
        st.info("Make sure the backend API server is running.")

# Footer
st.markdown("---")
st.markdown("*Lost & Found Portal - Connecting people with their belongings*")
>>>>>>> fcc5234e34f14b5777659aa45c3d42d7b218e475
