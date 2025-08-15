from PIL import Image, ImageFilter, ImageStat
import uuid
import os
import numpy as np
from typing import List, Tuple
import hashlib

def save_image(file) -> str:
    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)
    
    contents = file.file.read()
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join("images", filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return filepath

def extract_features(image_path: str) -> np.ndarray:
    """Extract simple color and texture features from an image for similarity matching"""
    try:
        # Open image with PIL
        img = Image.open(image_path)
        
        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize for consistent feature extraction
        img = img.resize((64, 64))
        
        # Extract color histogram features
        # Get RGB histograms
        r_hist = np.array(img.split()[0].histogram())
        g_hist = np.array(img.split()[1].histogram())
        b_hist = np.array(img.split()[2].histogram())
        
        # Normalize histograms
        r_hist = r_hist / np.sum(r_hist)
        g_hist = g_hist / np.sum(g_hist)
        b_hist = b_hist / np.sum(b_hist)
        
        # Get basic statistics
        stats = ImageStat.Stat(img)
        mean_rgb = np.array(stats.mean)
        std_rgb = np.array(stats.stddev)
        
        # Combine features
        features = np.concatenate([
            r_hist[:64],  # Reduced histogram bins
            g_hist[:64],
            b_hist[:64],
            mean_rgb,
            std_rgb
        ])
        
        return features.astype(np.float32)
        
    except Exception as e:
        print(f"Error extracting features from {image_path}: {e}")
        return np.array([])

def compare_images(img1_path: str, img2_path: str) -> float:
    """Compare two images and return similarity score (0-1, higher is more similar)"""
    try:
        # Extract features from both images
        features1 = extract_features(img1_path)
        features2 = extract_features(img2_path)
        
        if len(features1) == 0 or len(features2) == 0:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        cosine_similarity = dot_product / (norm1 * norm2)
        
        # Convert to 0-1 range (cosine similarity is -1 to 1)
        similarity = (cosine_similarity + 1) / 2
        
        return max(0.0, min(1.0, similarity))
            
    except Exception as e:
        print(f"Error comparing images {img1_path} and {img2_path}: {e}")
        return 0.0

def find_similar_images(query_image_path: str, all_image_paths: List[str], threshold: float = 0.1) -> List[Tuple[str, float]]:
    """Find images similar to the query image"""
    similar_images = []
    
    for img_path in all_image_paths:
        if img_path != query_image_path and os.path.exists(img_path):
            similarity = compare_images(query_image_path, img_path)
            if similarity > threshold:
                similar_images.append((img_path, similarity))
    
    # Sort by similarity score (descending)
    similar_images.sort(key=lambda x: x[1], reverse=True)
    return similar_images
