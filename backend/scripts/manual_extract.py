"""
Manual extraction script for when Kaggle CLI doesn't work
"""
import os
import zipfile
import shutil

def extract_manual_download():
    """Extract manually downloaded dataset"""
    
    zip_path = '../data/raw/crops-disease-dataset.zip'
    extract_path = '../data/raw/'
    
    if not os.path.exists(zip_path):
        print(f"❌ Please download the dataset manually and save it to:")
        print(f"   {os.path.abspath(zip_path)}")
        print("\nDownload from: https://www.kaggle.com/datasets/vishesh2395/crops-disease-dataset")
        return False
    
    print(f"📦 Found zip file: {zip_path}")
    print("Extracting...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print("✅ Extraction complete!")
        
        # Organize files
        organize_files()
        
        # Clean up
        os.remove(zip_path)
        print("🧹 Cleaned up zip file")
        
        return True
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

def organize_files():
    """Organize extracted files into correct structure"""
    
    # Look for the Final_Dataset folder
    possible_paths = [
        '../data/raw/Final_Dataset',
        '../data/raw/crops-disease-dataset/Final_Dataset',
        '../data/raw/archive/Final_Dataset'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            if path != '../data/raw/Final_Dataset':
                # Move contents to correct location
                print(f"Moving files from {path}...")
                for item in os.listdir(path):
                    src = os.path.join(path, item)
                    dst = os.path.join('../data/raw/Final_Dataset', item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
            break
    
    # Verify structure
    wheat_path = '../data/raw/Final_Dataset/Wheat'
    rice_path = '../data/raw/Final_Dataset/Rice'
    
    if os.path.exists(wheat_path) and os.path.exists(rice_path):
        print("✅ Dataset organized successfully!")
        
        # Count classes
        wheat_classes = len([d for d in os.listdir(wheat_path) 
                           if os.path.isdir(os.path.join(wheat_path, d))])
        rice_classes = len([d for d in os.listdir(rice_path) 
                          if os.path.isdir(os.path.join(rice_path, d))])
        
        print(f"   Wheat: {wheat_classes} classes")
        print(f"   Rice: {rice_classes} classes")
    else:
        print("⚠️ Dataset structure may need manual organization")

if __name__ == "__main__":
    extract_manual_download()