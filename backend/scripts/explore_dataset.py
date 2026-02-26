"""
Explore the Indian Crops Disease Dataset
Run this to understand what data we have
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Use absolute path to avoid any confusion
BASE_PATH = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
WHEAT_PATH = os.path.join(BASE_PATH, 'Wheat')
RICE_PATH = os.path.join(BASE_PATH, 'Rice')

print(f"📂 Dataset path: {BASE_PATH}")
print(f"🌾 Wheat path exists: {os.path.exists(WHEAT_PATH)}")
print(f"🌾 Rice path exists: {os.path.exists(RICE_PATH)}")
print("=" * 60)

def count_images(directory):
    """Count number of images in a directory and subdirectories"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                count += 1
    return count

def explore_dataset():
    """Main exploration function"""
    print("\n📊 WHEAT DATASET")
    print("-" * 40)
    
    # Get wheat classes
    wheat_classes = [d for d in os.listdir(WHEAT_PATH) 
                    if os.path.isdir(os.path.join(WHEAT_PATH, d))]
    
    print(f"Number of disease classes: {len(wheat_classes)}")
    
    # Count images per class
    wheat_counts = {}
    for class_name in sorted(wheat_classes):
        class_path = os.path.join(WHEAT_PATH, class_name)
        num_images = count_images(class_path)
        wheat_counts[class_name] = num_images
        print(f"  {class_name:30}: {num_images:4d} images")
    
    total_wheat = sum(wheat_counts.values())
    print(f"\n  {'TOTAL':30}: {total_wheat:4d} images")
    
    # Get rice classes
    print("\n\n📊 RICE DATASET")
    print("-" * 40)
    rice_classes = [d for d in os.listdir(RICE_PATH) 
                   if os.path.isdir(os.path.join(RICE_PATH, d))]
    
    print(f"Number of disease classes: {len(rice_classes)}")
    
    # Count images per class
    rice_counts = {}
    for class_name in sorted(rice_classes):
        class_path = os.path.join(RICE_PATH, class_name)
        num_images = count_images(class_path)
        rice_counts[class_name] = num_images
        print(f"  {class_name:30}: {num_images:4d} images")
    
    total_rice = sum(rice_counts.values())
    print(f"\n  {'TOTAL':30}: {total_rice:4d} images")
    
    # Overall stats
    print("\n\n📈 OVERALL STATISTICS")
    print("-" * 40)
    print(f"Total images: {total_wheat + total_rice}")
    print(f"Total classes: {len(wheat_classes) + len(rice_classes)}")
    print(f"  - Wheat: {len(wheat_classes)} classes")
    print(f"  - Rice: {len(rice_classes)} classes")
    
    # Plot distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Wheat distribution
    ax1.bar(range(len(wheat_counts)), list(wheat_counts.values()))
    ax1.set_title('Wheat Disease Classes Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Disease Class')
    ax1.set_ylabel('Number of Images')
    ax1.set_xticks(range(len(wheat_counts)))
    ax1.set_xticklabels([name.replace('Wheat_', '') for name in wheat_counts.keys()], 
                        rotation=45, ha='right', fontsize=8)
    
    # Add value labels on bars
    for i, (k, v) in enumerate(wheat_counts.items()):
        ax1.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=8)
    
    # Rice distribution
    ax2.bar(range(len(rice_counts)), list(rice_counts.values()), color='orange')
    ax2.set_title('Rice Disease Classes Distribution', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Disease Class')
    ax2.set_ylabel('Number of Images')
    ax2.set_xticks(range(len(rice_counts)))
    ax2.set_xticklabels([name.replace('Rice_', '') for name in rice_counts.keys()], 
                        rotation=45, ha='right', fontsize=10)
    
    # Add value labels on bars
    for i, (k, v) in enumerate(rice_counts.items()):
        ax2.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Save the plot
    plots_dir = os.path.join(os.path.dirname(BASE_PATH), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    plt.savefig(os.path.join(plots_dir, 'dataset_distribution.png'), 
                dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"\n✅ Exploration complete! Distribution plot saved to: {plots_dir}")
    
    return wheat_counts, rice_counts

def show_sample_images():
    """Display sample images from each class"""
    print("\n\n🖼️  SAMPLE IMAGES")
    print("-" * 40)
    
    # Create figure for wheat samples
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.ravel()
    
    # Show wheat samples
    wheat_classes = [d for d in os.listdir(WHEAT_PATH) 
                    if os.path.isdir(os.path.join(WHEAT_PATH, d))][:4]
    
    for idx, class_name in enumerate(wheat_classes):
        class_path = os.path.join(WHEAT_PATH, class_name)
        images = [f for f in os.listdir(class_path) 
                 if f.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'))]
        
        if images:
            img_path = os.path.join(class_path, images[0])
            img = Image.open(img_path)
            axes[idx].imshow(img)
            axes[idx].set_title(f"Wheat: {class_name.replace('Wheat_', '')}", fontsize=10)
            axes[idx].axis('off')
    
    # Show rice samples
    rice_classes = [d for d in os.listdir(RICE_PATH) 
                   if os.path.isdir(os.path.join(RICE_PATH, d))][:4]
    
    for idx, class_name in enumerate(rice_classes):
        class_path = os.path.join(RICE_PATH, class_name)
        images = [f for f in os.listdir(class_path) 
                 if f.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'))]
        
        if images:
            img_path = os.path.join(class_path, images[0])
            img = Image.open(img_path)
            axes[idx+4].imshow(img)
            axes[idx+4].set_title(f"Rice: {class_name.replace('Rice_', '')}", fontsize=10)
            axes[idx+4].axis('off')
    
    plt.suptitle('Sample Images from Dataset', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    plots_dir = os.path.join(os.path.dirname(BASE_PATH), 'plots')
    plt.savefig(os.path.join(plots_dir, 'sample_images.png'), dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Run exploration
    wheat_counts, rice_counts = explore_dataset()
    
    # Show sample images
    show_sample_images()
    
    print("\n" + "=" * 60)
    print("✅ DATASET EXPLORATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Create data generators for training")
    print("2. Build the CNN model")
    print("3. Train the model on this dataset")