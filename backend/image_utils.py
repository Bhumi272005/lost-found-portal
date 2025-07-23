import cv2
import uuid
import os
import numpy as np
from typing import List, Tuple

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
    """Extract ORB features from an image for similarity matching"""
    try:
        # Read image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return np.array([])
        
        # Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=500)
        
        # Find keypoints and descriptors
        keypoints, descriptors = orb.detectAndCompute(img, None)
        
        if descriptors is not None:
            return descriptors
        else:
            return np.array([])
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
        
        # Use FLANN matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Convert to float32 for FLANN
        features1 = features1.astype(np.float32)
        features2 = features2.astype(np.float32)
        
        matches = flann.knnMatch(features1, features2, k=2)
        
        # Apply Lowe's ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
        
        # Calculate similarity score
        if len(features1) > 0:
            similarity = len(good_matches) / len(features1)
            return min(similarity, 1.0)
        else:
            return 0.0
            
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
