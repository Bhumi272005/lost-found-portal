"""
Simple startup script for Lost and Found Portal
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        import pymongo
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 To fix this:")
        print("1. For local MongoDB: Install and run 'mongod --dbpath data\\db'")
        print("2. For MongoDB Atlas: Update .env with your connection string")
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting Backend Server...")
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    return subprocess.Popen(cmd)

def start_frontend():
    """Start the frontend"""
    print("🎨 Starting Frontend...")
    cmd = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"]
    return subprocess.Popen(cmd)

def main():
    print("🔍 Lost & Found Portal")
    print("=" * 40)
    
    if not check_mongodb():
        return
    
    print("\n🚀 Starting application...")
    
    backend_process = start_backend()
    frontend_process = start_frontend()
    
    print("\n✅ Application started!")
    print("🌐 Frontend: http://localhost:8501")
    print("🔧 Backend: http://localhost:8000")
    print("\n📝 Press Ctrl+C to stop")
    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
