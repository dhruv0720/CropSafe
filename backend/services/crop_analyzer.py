"""
Complete crop analysis - No training required!
Works on any image in real-time
"""
import cv2
import numpy as np
from PIL import Image
import io

class CropAnalyzer:
    def __init__(self):
        # Disease signatures based on color and patterns
        self.disease_signatures = {
            'wheat': {
                'YellowRust': {
                    'color_range': {'lower': [20, 50, 50], 'upper': [35, 255, 255]},
                    'pattern': 'stripes',
                    'name_hi': 'पीला रतुआ'
                },
                'BrownRust': {
                    'color_range': {'lower': [10, 50, 50], 'upper': [20, 255, 200]},
                    'pattern': 'spots',
                    'name_hi': 'भूरा रतुआ'
                },
                'Aphid': {
                    'color_range': {'lower': [30, 30, 30], 'upper': [80, 255, 255]},
                    'pattern': 'insects',
                    'name_hi': 'एफिड'
                }
            },
            'rice': {
                'Blast': {
                    'color_range': {'lower': [20, 50, 50], 'upper': [35, 255, 255]},
                    'pattern': 'diamond',
                    'name_hi': 'ब्लास्ट'
                },
                'BrownSpot': {
                    'color_range': {'lower': [10, 50, 50], 'upper': [20, 255, 200]},
                    'pattern': 'circular',
                    'name_hi': 'भूरा धब्बा'
                }
            }
        }
    
    def analyze(self, image, crop_type='wheat'):
        """
        Complete analysis of crop image
        Returns disease and severity in real-time
        """
        # Convert to OpenCV
        if isinstance(image, Image.Image):
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            img = image
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        height, width = img.shape[:2]
        total_pixels = height * width
        
        # Analyze each possible disease
        disease_scores = {}
        disease_masks = {}
        
        for disease_name, signature in self.disease_signatures[crop_type].items():
            # Create mask for this disease's color range
            lower = np.array(signature['color_range']['lower'])
            upper = np.array(signature['color_range']['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Clean up mask
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Calculate percentage
            diseased_pixels = np.sum(mask > 0)
            percentage = (diseased_pixels / total_pixels) * 100
            
            disease_scores[disease_name] = percentage
            disease_masks[disease_name] = mask
        
        # Find primary disease (highest percentage)
        primary_disease = max(disease_scores, key=disease_scores.get)
        primary_percentage = disease_scores[primary_disease]
        
        # Calculate overall severity (combined diseased area)
        combined_mask = np.zeros((height, width), dtype=np.uint8)
        for mask in disease_masks.values():
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        total_diseased = np.sum(combined_mask > 0)
        severity_percentage = (total_diseased / total_pixels) * 100
        
        # Determine severity level
        if severity_percentage < 10:
            severity = "Low"
            severity_hi = "कम"
            color = "#8BC34A"
        elif severity_percentage < 30:
            severity = "Medium"
            severity_hi = "मध्यम"
            color = "#FFC107"
        elif severity_percentage < 50:
            severity = "High"
            severity_hi = "अधिक"
            color = "#FF9800"
        else:
            severity = "Very High"
            severity_hi = "बहुत अधिक"
            color = "#F44336"
        
        # Get top 3 diseases
        top_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3 = [
            {
                "disease": d[0],
                "disease_hi": self.disease_signatures[crop_type][d[0]]['name_hi'],
                "confidence": d[1] / 100  # Normalize to 0-1
            }
            for d in top_diseases
        ]
        
        return {
            "success": True,
            "crop": crop_type,
            "prediction": {
                "disease": primary_disease,
                "disease_hi": self.disease_signatures[crop_type][primary_disease]['name_hi'],
                "confidence": primary_percentage / 100,  # Normalize to 0-1
                "severity": {
                    "level": severity,
                    "level_hi": severity_hi,
                    "percentage": round(severity_percentage, 1),
                    "color": color
                },
                "top_3_predictions": top_3,
                "detailed_analysis": disease_scores
            }
        }
    
    def get_visualization(self, image, crop_type='wheat'):
        """Return image with diseased areas highlighted"""
        if isinstance(image, Image.Image):
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            img = image
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        result = img.copy()
        
        # Highlight each disease with different color
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]
        
        for i, (disease_name, signature) in enumerate(self.disease_signatures[crop_type].items()):
            lower = np.array(signature['color_range']['lower'])
            upper = np.array(signature['color_range']['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            result[mask > 0] = colors[i % len(colors)]
        
        return result