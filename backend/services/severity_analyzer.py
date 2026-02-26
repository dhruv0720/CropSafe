"""
Image-based severity analysis - Works immediately, no training needed!
"""
import cv2
import numpy as np
from PIL import Image
import io

class SeverityAnalyzer:
    def __init__(self):
        # Color ranges for disease detection (tuned for wheat/rice)
        self.disease_ranges = [
            # Yellow/Brown spots (common in rust, blast)
            {'lower': [20, 50, 50], 'upper': [35, 255, 255]},  # Yellow
            {'lower': [10, 50, 20], 'upper': [20, 255, 200]},  # Brown
            {'lower': [0, 50, 50], 'upper': [10, 255, 200]},   # Dark brown
        ]
    
    def analyze(self, image):
        """
        Analyze disease severity using color segmentation
        Returns severity level and percentage
        """
        # Convert PIL to OpenCV if needed
        if isinstance(image, Image.Image):
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            img = image
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Create combined mask for all disease colors
        disease_mask = np.zeros(img.shape[:2], dtype=np.uint8)
        
        for color_range in self.disease_ranges:
            lower = np.array(color_range['lower'])
            upper = np.array(color_range['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            disease_mask = cv2.bitwise_or(disease_mask, mask)
        
        # Clean up mask
        kernel = np.ones((5,5), np.uint8)
        disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_OPEN, kernel)
        disease_mask = cv2.morphologyEx(disease_mask, cv2.MORPH_CLOSE, kernel)
        
        # Calculate percentage
        total_pixels = disease_mask.shape[0] * disease_mask.shape[1]
        diseased_pixels = np.sum(disease_mask > 0)
        percentage = (diseased_pixels / total_pixels) * 100
        
        # Determine severity level
        if percentage < 10:
            level = "Low"
            level_hi = "कम"
            color = "#8BC34A"
            description = "Minor infection, early stage"
            description_hi = "मामूली संक्रमण, शुरुआती अवस्था"
        elif percentage < 30:
            level = "Medium"
            level_hi = "मध्यम"
            color = "#FFC107"
            description = "Moderate infection, take action"
            description_hi = "मध्यम संक्रमण, उपचार करें"
        elif percentage < 50:
            level = "High"
            level_hi = "अधिक"
            color = "#FF9800"
            description = "Severe infection, immediate action needed"
            description_hi = "गंभीर संक्रमण, तुरंत उपचार करें"
        else:
            level = "Very High"
            level_hi = "बहुत अधिक"
            color = "#F44336"
            description = "Very severe, crop loss risk"
            description_hi = "अति गंभीर, फसल हानि का जोखिम"
        
        return {
            "level": level,
            "level_hi": level_hi,
            "percentage": round(percentage, 1),
            "color": color,
            "description": description,
            "description_hi": description_hi,
            "method": "image_analysis",
            "diseased_pixels": int(diseased_pixels),
            "total_pixels": total_pixels
        }
    
    def get_visualization(self, image):
        """Return image with diseased areas highlighted"""
        if isinstance(image, Image.Image):
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            img = image
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Create mask
        disease_mask = np.zeros(img.shape[:2], dtype=np.uint8)
        for color_range in self.disease_ranges:
            lower = np.array(color_range['lower'])
            upper = np.array(color_range['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            disease_mask = cv2.bitwise_or(disease_mask, mask)
        
        # Create red highlight for diseased areas
        result = img.copy()
        result[disease_mask > 0] = [0, 0, 255]  # Red in BGR
        
        return result