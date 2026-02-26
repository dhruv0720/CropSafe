"""
Debug script to find the exact dataset path
"""
import os

print("🔍 Searching for dataset...")
print("=" * 60)

# Start from the backend directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Backend directory: {base_dir}")

# Check data/raw
raw_dir = os.path.join(base_dir, 'data', 'raw')
print(f"\nChecking: {raw_dir}")
print(f"Exists: {os.path.exists(raw_dir)}")

if os.path.exists(raw_dir):
    print("\nContents of raw directory:")
    for item in os.listdir(raw_dir):
        item_path = os.path.join(raw_dir, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
            # Look one level deeper
            for subitem in os.listdir(item_path)[:5]:  # Show first 5
                subpath = os.path.join(item_path, subitem)
                if os.path.isdir(subpath):
                    print(f"      📁 {subitem}/")
                else:
                    print(f"      📄 {subitem}")
        else:
            print(f"  📄 {item}")

# Also check if there's an 'archive' folder anywhere
print("\n🔎 Searching for 'Wheat' folders...")
for root, dirs, files in os.walk(base_dir):
    if 'Wheat' in dirs:
        print(f"✅ Found Wheat at: {root}")
        wheat_path = os.path.join(root, 'Wheat')
        classes = [d for d in os.listdir(wheat_path) 
                  if os.path.isdir(os.path.join(wheat_path, d))]
        print(f"   Classes found: {classes[:5]}...")  # Show first 5
    if 'Rice' in dirs:
        print(f"✅ Found Rice at: {root}")