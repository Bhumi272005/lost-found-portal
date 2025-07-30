# MongoDB GUI Setup for Viewing Images

## 1. MongoDB Compass (Official GUI - Recommended)

### Installation
1. Download MongoDB Compass from: https://www.mongodb.com/products/compass
2. Install the application on your computer
3. Launch MongoDB Compass

### Connection Setup
- **Connection String**: `mongodb://localhost:27017/` (for local MongoDB)
- **Or for MongoDB Atlas**: `mongodb+srv://username:password@cluster.mongodb.net/`
- Click "Connect"

### Viewing Images in GridFS
1. **Select Database**: Choose `lost_and_found` database
2. **Find GridFS Collections**: Look for collections named:
   - `fs.files` - Contains image metadata (filename, upload date, file ID)
   - `fs.chunks` - Contains the actual image data chunks
3. **View Image Information**:
   - Click on `fs.files` collection
   - You'll see all uploaded images with their metadata
   - Each document shows: `_id`, `filename`, `uploadDate`, `length`, etc.

### Image Export from Compass
1. Go to `fs.files` collection
2. Click on a document to see its details
3. Copy the `_id` value (this is your file_id)
4. Use the file_id in the web app or API to view the actual image

## 2. MongoDB Shell Commands

### Connect to MongoDB Shell
```bash
# For local MongoDB
mongo

# For MongoDB Atlas
mongo "mongodb+srv://cluster.mongodb.net/myFirstDatabase" --username <username>
```

### View Image Metadata
```javascript
// Use your database
use lost_and_found

// List all images with details
db.fs.files.find().pretty()

// Count total images
db.fs.files.count()

// Find images by filename
db.fs.files.find({"filename": /jpg/}).pretty()

// Get specific image info by ID
db.fs.files.find({"_id": ObjectId("your_file_id_here")})
```

## 3. Studio 3T (Alternative GUI)

### Free Version Available
1. Download from: https://studio3t.com/
2. Install and create free account
3. Connect using same connection string
4. Browse to `lost_and_found` database
5. View `fs.files` and `fs.chunks` collections

## 4. Web-based MongoDB Admin (For Network Access)

### Mongo Express (Web Interface)
```bash
# Install mongo-express globally
npm install -g mongo-express

# Run mongo-express
mongo-express

# Access via browser: http://localhost:8081
```

## 5. Robo 3T (Lightweight GUI)

### Free Community Version
1. Download from: https://robomongo.org/
2. Install and setup connection
3. Browse database collections
4. View GridFS files in `fs.files` collection

## Network Access for Other Users

### For Local MongoDB Network Access:
1. **Configure MongoDB** to accept external connections:
   - Edit `mongod.conf` file
   - Set `bindIp: 0.0.0.0` (allows all IPs)
   - Restart MongoDB service

2. **Firewall Settings**:
   - Allow port 27017 in Windows Firewall
   - `netsh advfirewall firewall add rule name="MongoDB" dir=in action=allow protocol=TCP localport=27017`

3. **Connection String for Other Computers**:
   - Find your IP: `ipconfig`
   - Other users connect with: `mongodb://YOUR_IP:27017/`

### For MongoDB Atlas (Cloud):
- All users can connect with the same Atlas connection string
- No firewall configuration needed
- Works from any internet-connected computer

## Image Viewing Workflow

1. **In GUI Tool**: View `fs.files` collection to see image metadata
2. **Get File ID**: Copy the `_id` from the document
3. **View Image**: Use one of these methods:
   - Web App: Go to Search Items page
   - Direct API: `http://localhost:8000/images/{file_id}`
   - Export Script: Use the export function to save images locally

## Security Notes

- **Local MongoDB**: Only use `bindIp: 0.0.0.0` in trusted networks
- **MongoDB Atlas**: Use strong passwords and IP whitelisting
- **Production**: Always use authentication and SSL/TLS encryption
