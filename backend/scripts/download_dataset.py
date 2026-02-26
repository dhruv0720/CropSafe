"""
Script to download the Indian Crops Disease Dataset
"""
import os
import zipfile
import requests
from tqdm import tqdm
import kaggle

def download_from_kaggle():
    """Download dataset from Kaggle"""
    print("📥 Downloading Indian Crops Disease Dataset...")
    
    # Option 1: Using Kaggle API (if you have kaggle.json configured)
    try:
        kaggle.api.dataset_download_files(
            'vishesh2395/crops-disease-dataset',
            path='./data/raw',
            unzip=True
        )
        print("✅ Dataset downloaded successfully via Kaggle API!")
        return True
    except:
        print("⚠️ Kaggle API failed, trying direct download...")
        return False

def download_direct():
    """Alternative: Direct download if Kaggle API fails"""
    # This is a placeholder - we'll need the actual direct link
    # For now, let's create a manual instruction
    print("""
    📌 Manual Download Required:
    
    1. Go to: https://www.kaggle.com/datasets/vishesh2395/crops-disease-dataset
    2. Click 'Download' (requires Kaggle login)
    3. Extract the zip file to: backend/data/raw/
    
    The dataset should contain:
    - Wheat/ (15 classes)
    - Rice/ (4 classes)
    """)
    return False

def verify_dataset():
    """Check if dataset was downloaded correctly"""
    wheat_path = './data/raw/Final_Dataset/Wheat'
    rice_path = './data/raw/Final_Dataset/Rice'
    
    if os.path.exists(wheat_path) and os.path.exists(rice_path):
        wheat_classes = len([d for d in os.listdir(wheat_path) 
                           if os.path.isdir(os.path.join(wheat_path, d))])
        rice_classes = len([d for d in os.listdir(rice_path) 
                          if os.path.isdir(os.path.join(rice_path, d))])
        
        print(f"\n✅ Dataset verified!")
        print(f"   - Wheat: {wheat_classes} disease classes")
        print(f"   - Rice: {rice_classes} disease classes")
        
        # Count images
        wheat_images = sum([len(files) for r, d, files in os.walk(wheat_path)])
        rice_images = sum([len(files) for r, d, files in os.walk(rice_path)])
        print(f"   - Total images: {wheat_images + rice_images}")
        
        return True
    else:
        print("❌ Dataset not found in expected location")
        return False

if __name__ == "__main__":
    # Create data directories
    os.makedirs('./data/raw', exist_ok=True)
    os.makedirs('./data/processed', exist_ok=True)
    
    # Try downloading
    if not download_from_kaggle():
        download_direct()
    
    # Verify
    verify_dataset()