"""
Auto-label severity based on color segmentation
This will automatically analyze all images and assign severity labels
"""
import cv2
import numpy as np
import os
from PIL import Image
import shutil
from tqdm import tqdm

class AutoSeverityLabeler:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.output_path = os.path.join(os.path.dirname(dataset_path), 'severity_dataset_auto')
        
        # Create output directories
        for severity in ['Low', 'Medium', 'High', 'Very High']:
            os.makedirs(os.path.join(self.output_path, severity), exist_ok=True)
    
    def calculate_disease_percentage(self, image_path):
        """
        Calculate percentage of leaf area affected by disease
        Uses color segmentation to identify diseased spots
        """
        # Read image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        
        # Define color ranges for diseased tissue (yellow/brown spots)
        # These ranges can be adjusted based on your specific diseases
        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([35, 255, 255])
        
        lower_brown = np.array([10, 50, 20])
        upper_brown = np.array([20, 255, 200])
        
        # Create masks for diseased areas
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        
        # Combine masks
        disease_mask = cv2.bitwise_or(mask_yellow, mask_brown)
        
        # Apply some morphological operations to clean up the mask
        kernel = np.ones((5,5), np.uint8)
        disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_OPEN, kernel)
        disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_CLOSE, kernel)
        
        # Calculate percentage
        total_pixels = disease_mask.shape[0] * disease_mask.shape[1]
        diseased_pixels = np.sum(disease_mask > 0)
        percentage = (diseased_pixels / total_pixels) * 100
        
        return percentage
    
    def get_severity_from_percentage(self, percentage):
        """Convert percentage to severity level"""
        if percentage < 10:
            return 'Low'
        elif percentage < 30:
            return 'Medium'
        elif percentage < 50:
            return 'High'
        else:
            return 'Very High'
    
    def auto_label_all_images(self):
        """Auto-label all images in the dataset"""
        print("=" * 60)
        print("🤖 AUTO SEVERITY LABELING IN PROGRESS")
        print("=" * 60)
        
        # Collect all images from wheat and rice folders
        all_images = []
        
        # Wheat
        wheat_path = os.path.join(self.dataset_path, 'Wheat')
        if os.path.exists(wheat_path):
            for disease in os.listdir(wheat_path):
                disease_path = os.path.join(wheat_path, disease)
                if os.path.isdir(disease_path):
                    for img in os.listdir(disease_path):
                        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                            all_images.append(os.path.join(disease_path, img))
        
        # Rice
        rice_path = os.path.join(self.dataset_path, 'Rice')
        if os.path.exists(rice_path):
            for disease in os.listdir(rice_path):
                disease_path = os.path.join(rice_path, disease)
                if os.path.isdir(disease_path):
                    for img in os.listdir(disease_path):
                        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                            all_images.append(os.path.join(disease_path, img))
        
        print(f"📸 Found {len(all_images)} images to process")
        
        # Process each image
        severity_counts = {'Low': 0, 'Medium': 0, 'High': 0, 'Very High': 0}
        
        for img_path in tqdm(all_images, desc="Processing images"):
            try:
                # Calculate disease percentage
                percentage = self.calculate_disease_percentage(img_path)
                
                # Get severity level
                severity = self.get_severity_from_percentage(percentage)
                
                # Copy image to appropriate folder
                filename = os.path.basename(img_path)
                dest_path = os.path.join(self.output_path, severity, filename)
                
                # Add prefix if filename already exists
                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(filename)
                    dest_path = os.path.join(self.output_path, severity, f"{name}_{severity_counts[severity]}{ext}")
                
                shutil.copy2(img_path, dest_path)
                severity_counts[severity] += 1
                
            except Exception as e:
                print(f"❌ Error processing {img_path}: {e}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ AUTO LABELING COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Severity Distribution:")
        for severity, count in severity_counts.items():
            percentage = (count / len(all_images)) * 100
            print(f"  {severity:10}: {count:4d} images ({percentage:.1f}%)")
        
        print(f"\n📁 Images saved to: {self.output_path}")
        
        return severity_counts

if __name__ == "__main__":
    dataset_path = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
    labeler = AutoSeverityLabeler(dataset_path)
    labeler.auto_label_all_images()