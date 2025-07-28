"""
MongoDB Setup and Connection Test for Lost & Found Portal
Run this script to test your MongoDB connection before starting the application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from pymongo import MongoClient
        
        # Get MongoDB URL from environment or use default
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "lost_and_found")
        
        print("🔄 Testing MongoDB connection...")
        print(f"📍 Connecting to: {MONGO_URL}")
        print(f"📂 Database: {DATABASE_NAME}")
        
        # Try to connect
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        
        # Test the connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get collection info
        collection = db["items"]
        count = collection.count_documents({})
        print(f"📊 Current items in database: {count}")
        
        # List all databases (optional)
        db_list = client.list_database_names()
        print(f"📚 Available databases: {', '.join(db_list)}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 Solutions:")
        print("1. Local MongoDB:")
        print("   - Install MongoDB Community Edition")
        print("   - Start MongoDB service: net start MongoDB")
        print("   - Set MONGO_URL=mongodb://localhost:27017/")
        print()
        print("2. MongoDB Atlas (Cloud):")
        print("   - Create free cluster at https://www.mongodb.com/atlas")
        print("   - Get connection string")
        print("   - Set MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/")
        print()
        print("3. Environment Configuration:")
        print("   - Create .env file with:")
        print("     MONGO_URL=your_mongodb_connection_string")
        print("     DATABASE_NAME=lost_and_found")
        return False

def setup_environment():
    """Help user set up environment file"""
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("🔧 Creating .env file...")
        
        # Ask user for MongoDB URL
        print("\n📝 MongoDB Setup Options:")
        print("1. Local MongoDB: mongodb://localhost:27017/")
        print("2. MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/")
        print("3. Custom URL")
        
        choice = input("\nSelect option (1/2/3): ").strip()
        
        if choice == "1":
            mongo_url = "mongodb://localhost:27017/"
        elif choice == "2":
            mongo_url = input("Enter your MongoDB Atlas connection string: ").strip()
        elif choice == "3":
            mongo_url = input("Enter your MongoDB URL: ").strip()
        else:
            mongo_url = "mongodb://localhost:27017/"
        
        # Create .env file
        with open(env_path, "w") as f:
            f.write(f"# MongoDB Configuration\n")
            f.write(f"MONGO_URL={mongo_url}\n")
            f.write(f"DATABASE_NAME=lost_and_found\n\n")
            f.write(f"# API Configuration\n")
            f.write(f"API_URL=http://localhost:8000\n\n")
            f.write(f"# Optional: Gemini API Key for image classification\n")
            f.write(f"# GEMINI_API_KEY=your_gemini_api_key_here\n")
        
        print(f"✅ Created {env_path} file")
    else:
        print(f"✅ {env_path} file already exists")

if __name__ == "__main__":
    print("🚀 Lost & Found Portal - MongoDB Setup")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    print()
    
    # Test connection
    success = test_mongodb_connection()
    print()
    
    if success:
        print("🎉 MongoDB is ready! You can now start your application:")
        print("   python backend/main.py")
    else:
        print("⚠️ Please fix MongoDB connection before starting the application.")
        print("📖 See the solutions above or check MONGODB_SETUP.md for detailed instructions.")
