/* global use, db */
/**
 * Lost and Found Portal - Image URL Shareability Checker
 * 
 * Repository: https://github.com/Bhumi272005/lost-found-portal
 * Purpose: Analyze if stored image URLs are shareable across different networks
 * 
 * WHAT THIS SCRIPT DOES:
 * - Connects to your Lost and Found MongoDB database
 * - Analyzes all image URLs to determine shareability
 * - Provides recommendations for making URLs globally accessible
 * 
 * SHAREABILITY LEVELS:
 * ❌ Localhost (127.0.0.1, localhost) - Only accessible on your computer
 * ⚠️  Local Network (192.168.x.x) - Accessible on same WiFi network  
 * ✅ Global (https://domain.com) - Accessible from anywhere on internet
 * 
 * SETUP REQUIREMENTS:
 * 1. MongoDB running locally (mongodb://localhost:27017)
 * 2. Lost and Found app with some reported items containing images
 * 3. MongoDB Compass or VS Code with MongoDB extension
 * 
 * HOW TO RUN:
 * - In MongoDB Compass: Copy this code → Queries tab → Run
 * - In VS Code: Open file → Right-click → "Run MongoDB Playground"
 * 
 * @author Bhumi272005
 * @version 1.0
 */

// MongoDB Playground for Lost and Found Portal
// GitHub Repository: https://github.com/Bhumi272005/lost-found-portal
// This playground checks if your image URLs are shareable across networks

// SETUP INSTRUCTIONS:
// 1. Make sure MongoDB is running locally (mongodb://localhost:27017)
// 2. Ensure your Lost and Found app has created some items with images
// 3. Run this playground in MongoDB Compass or VS Code MongoDB extension

// Connect to your Lost and Found database
// Change 'lost_and_found' to your actual database name if different
use('lost_and_found');

// 1. Check if database exists and has items
console.log("=== DATABASE INFO ===");
console.log("📊 Lost and Found Portal - Database Analysis");
console.log("🔗 Repository: https://github.com/Bhumi272005/lost-found-portal");
console.log("Database:", db.getName());
console.log("Collections:", db.getCollectionNames());

// 2. Count total items
const totalItems = db.items.countDocuments();
console.log("Total items in database:", totalItems);

// 3. Check items with images
const itemsWithImages = db.items.countDocuments({ "image_url": { $exists: true, $ne: null } });
console.log("Items with images:", itemsWithImages);

console.log("\n=== SAMPLE ITEMS WITH IMAGES ===");

// 4. Show sample items with image URLs
db.items.find(
  { "image_url": { $exists: true, $ne: null } },
  { 
    "title": 1, 
    "image_url": 1, 
    "status": 1,
    "timestamp": 1,
    "_id": 0 
  }
).limit(5).forEach(item => {
  console.log(`Title: ${item.title}`);
  console.log(`Status: ${item.status}`);
  console.log(`Image URL: ${item.image_url}`);
  console.log(`Timestamp: ${item.timestamp}`);
  console.log("---");
});

console.log("\n=== IMAGE URL ANALYSIS ===");

// 5. Analyze URL patterns
const allImageUrls = db.items.distinct("image_url");
console.log("Total unique image URLs:", allImageUrls.length);

// Check URL patterns
let localhostCount = 0;
let networkCount = 0;
let globalCount = 0;

allImageUrls.forEach(url => {
  if (url && typeof url === 'string') {
    if (url.includes('localhost') || url.includes('127.0.0.1')) {
      localhostCount++;
    } else if (url.includes('192.168.') || url.includes('10.0.') || url.includes('172.')) {
      networkCount++;
    } else if (url.includes('https://') && !url.includes('192.168.') && !url.includes('localhost')) {
      globalCount++;
    }
  }
});

console.log("URL Shareability Analysis:");
console.log(`❌ Localhost URLs (not shareable): ${localhostCount}`);
console.log(`⚠️  Local network URLs (WiFi network only): ${networkCount}`);
console.log(`✅ Global URLs (internet accessible): ${globalCount}`);
console.log("");
console.log("📖 URL Shareability Guide:");
console.log("• Localhost (127.0.0.1, localhost) = Only your computer");
console.log("• Local Network (192.168.x.x) = Same WiFi network");  
console.log("• Global (https://domain.com) = Anywhere on internet");

console.log("\n=== SAMPLE IMAGE URLS ===");
// Show first few URLs for inspection
allImageUrls.slice(0, 3).forEach((url, index) => {
  if (url) {
    console.log(`${index + 1}. ${url}`);
    
    // Determine shareability status with detailed explanations
    if (url.includes('localhost') || url.includes('127.0.0.1')) {
      console.log("   Status: ❌ Not shareable (localhost only)");
      console.log("   📱 Can access: Only your computer");
    } else if (url.includes('192.168.') || url.includes('10.0.') || url.includes('172.')) {
      console.log("   Status: ⚠️  Local network only");
      console.log("   📱 Can access: Devices on same WiFi network");
    } else if (url.includes('https://') && !url.includes('192.168.') && !url.includes('localhost')) {
      console.log("   Status: ✅ Globally shareable");
      console.log("   📱 Can access: Anyone with internet connection");
    } else {
      console.log("   Status: ❓ Unknown pattern");
      console.log("   📱 Can access: Uncertain - please check manually");
    }
    console.log("");
  }
});

// 6. Check GridFS files (if using GridFS)
console.log("\n=== GRIDFS INFO ===");
try {
  const gridFSFiles = db.fs.files.countDocuments();
  console.log("GridFS files stored:", gridFSFiles);
  
  if (gridFSFiles > 0) {
    console.log("Sample GridFS files:");
    db.fs.files.find({}, { filename: 1, uploadDate: 1 }).limit(3).forEach(file => {
      console.log(`- ${file.filename} (${file.uploadDate})`);
    });
  }
} catch (e) {
  console.log("GridFS not found or no files");
}

console.log("\n=== RECOMMENDATIONS ===");
console.log("Current Analysis Results:");

if (globalCount === 0 && networkCount > 0) {
  console.log("� STATUS: Local Network URLs Detected");
  console.log("🏠 Your images are accessible within your local network only");
  console.log("");
  console.log("🚀 TO MAKE GLOBALLY SHAREABLE:");
  console.log("1. Deploy to cloud platform:");
  console.log("   • Railway: https://railway.app");
  console.log("   • Render: https://render.com");
  console.log("   • Heroku: https://heroku.com");
  console.log("");
  console.log("2. Set up MongoDB Atlas (cloud database):");
  console.log("   • Visit: https://mongodb.com/atlas");
  console.log("   • Create free cluster");
  console.log("");
  console.log("3. Update environment variables:");
  console.log("   • MONGO_URL=mongodb+srv://...");
  console.log("   • BASE_URL=https://your-app.railway.app");
  console.log("");
  console.log("📖 See DEPLOYMENT.md for detailed instructions");
} else if (globalCount > 0) {
  console.log("🎉 EXCELLENT! You have globally shareable URLs");
  console.log("✅ Your images can be accessed from anywhere on the internet");
} else if (localhostCount > 0) {
  console.log("⚠️  WARNING: Localhost URLs detected");
  console.log("❌ These URLs only work on your computer");
  console.log("🔧 Update BASE_URL in your environment to use network IP or deploy to cloud");
} else {
  console.log("❓ No image URLs found. Try uploading some items with images first.");
  console.log("💡 Make sure your Lost and Found app is running and you've reported items with photos");
}
