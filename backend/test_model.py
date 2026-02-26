# backend/test_model.py
"""
Test if model actually predicts differently for different images
"""
import tensorflow as tf
import numpy as np
from PIL import Image
import os

print("🔍 Testing Severity Model...")
print("=" * 50)

# Load your model
model_path = "severity_model_final.h5"
if not os.path.exists(model_path):
    model_path = "severity_model_stable.keras"
if not os.path.exists(model_path):
    model_path = "severity_model_best.keras"

model = tf.keras.models.load_model(model_path)
print(f"✅ Loaded model from: {model_path}")

# Get 3 different test images from your dataset
test_images = [
    r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto\Low\some_image.jpg",
    r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto\Medium\some_image.jpg",
    r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto\High\some_image.jpg"
]

# If above paths don't exist, find any 3 images
import glob
all_images = glob.glob(r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto\**\*.jpg", recursive=True)
test_images = all_images[:3] if len(all_images) >= 3 else all_images

print(f"\n📸 Testing {len(test_images)} images:")
print("-" * 50)

for i, img_path in enumerate(test_images):
    # Load and preprocess
    img = Image.open(img_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    predictions = model.predict(img_array, verbose=0)[0]
    severity = np.argmax(predictions)
    confidence = predictions[severity]
    
    severity_names = ['Low', 'Medium', 'High', 'Very High']
    
    print(f"Image {i+1}: {os.path.basename(img_path)}")
    print(f"  Predicted: {severity_names[severity]} ({confidence:.2%})")
    print(f"  Raw predictions: Low={predictions[0]:.2%}, Medium={predictions[1]:.2%}, High={predictions[2]:.2%}, Very High={predictions[3]:.2%}")
    print()