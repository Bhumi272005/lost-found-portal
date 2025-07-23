import sqlite3
from datetime import datetime
import pytz

def get_ist_timestamp():
    """Get current timestamp in Indian Standard Time"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            category TEXT,
            location TEXT,
            status TEXT,
            name TEXT,
            contact TEXT,
            image_path TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()

def insert_item(item, image_path):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    ist_timestamp = get_ist_timestamp()
    c.execute("""
        INSERT INTO items (title, description, category, location, status, name, contact, image_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (item.title, item.description, item.category, item.location, item.status, item.name, item.contact, image_path, ist_timestamp))
    conn.commit()
    conn.close()

def format_ist_timestamp(timestamp_str):
    """Format timestamp string to display IST time clearly"""
    try:
        # Parse the timestamp and ensure it's displayed as IST
        dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d-%m-%Y %H:%M:%S IST')
    except:
        return timestamp_str + ' IST'

def fetch_all_items():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY timestamp DESC")
    items = c.fetchall()
    conn.close()
    
    # Format timestamps to show IST clearly
    formatted_items = []
    for item in items:
        item_list = list(item)
        if len(item_list) > 9 and item_list[9]:  # timestamp is at index 9
            item_list[9] = format_ist_timestamp(item_list[9])
        formatted_items.append(tuple(item_list))
    
    return formatted_items

def search_items(query, status_filter=None):
    """Search items by title, description, or category"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    if status_filter and status_filter != "All":
        c.execute("""
            SELECT * FROM items 
            WHERE (title LIKE ? OR description LIKE ? OR category LIKE ?) 
            AND status = ?
            ORDER BY timestamp DESC
        """, (f"%{query}%", f"%{query}%", f"%{query}%", status_filter))
    else:
        c.execute("""
            SELECT * FROM items 
            WHERE title LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY timestamp DESC
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    
    items = c.fetchall()
    conn.close()
    
    # Format timestamps
    formatted_items = []
    for item in items:
        item_list = list(item)
        if len(item_list) > 9 and item_list[9]:
            item_list[9] = format_ist_timestamp(item_list[9])
        formatted_items.append(tuple(item_list))
    
    return formatted_items

def delete_item(item_id):
    """Delete an item by ID"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0
