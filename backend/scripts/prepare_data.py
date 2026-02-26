"""
Prepare data for training - Create data generators
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import pickle

# Use the same path we confirmed works
BASE_PATH = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
WHEAT_PATH = os.path.join(BASE_PATH, 'Wheat')
RICE_PATH = os.path.join(BASE_PATH, 'Rice')

# Create directories for saving models and training info
os.makedirs('../models', exist_ok=True)
os.makedirs('../models/training_history', exist_ok=True)

def create_data_generators(crop_path, crop_name, img_size=(224, 224), batch_size=32):
    """
    Create training and validation data generators with augmentation
    """
    print(f"\n🌱 Creating data generators for {crop_name}...")
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        validation_split=0.2  # 80% training, 20% validation
    )
    
    # Only rescaling for validation (no augmentation)
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        crop_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=42
    )
    
    # Validation generator
    validation_generator = val_datagen.flow_from_directory(
        crop_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )
    
    print(f"✅ {crop_name} generators created!")
    print(f"   Training samples: {train_generator.samples}")
    print(f"   Validation samples: {validation_generator.samples}")
    print(f"   Classes: {train_generator.class_indices}")
    
    # Save class indices for later use
    class_indices = train_generator.class_indices
    with open(f'../models/{crop_name}_class_indices.pkl', 'wb') as f:
        pickle.dump(class_indices, f)
    
    return train_generator, validation_generator, class_indices

def visualize_augmentation(crop_path, crop_name):
    """
    Visualize data augmentation on a sample image
    """
    print(f"\n🖼️  Visualizing data augmentation for {crop_name}...")
    
    # Create augmentation generator
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2]
    )
    
    # Get a sample image
    classes = [d for d in os.listdir(crop_path) 
               if os.path.isdir(os.path.join(crop_path, d))]
    sample_class = classes[0]
    class_path = os.path.join(crop_path, sample_class)
    sample_img = [f for f in os.listdir(class_path) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))][0]
    img_path = os.path.join(class_path, sample_img)
    
    # Load and prepare image
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array.reshape((1,) + img_array.shape)
    
    # Generate augmented images
    plt.figure(figsize=(15, 8))
    plt.suptitle(f'Data Augmentation Examples - {crop_name}', fontsize=16, fontweight='bold')
    
    # Show original
    plt.subplot(3, 4, 1)
    plt.imshow(img)
    plt.title('Original', fontsize=12)
    plt.axis('off')
    
    # Show 11 augmented versions
    for i, batch in enumerate(datagen.flow(img_array, batch_size=1)):
        if i >= 11:
            break
        plt.subplot(3, 4, i + 2)
        augmented_img = tf.keras.preprocessing.image.array_to_img(batch[0])
        plt.imshow(augmented_img)
        plt.title(f'Augmented {i+1}', fontsize=10)
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(f'../models/training_history/{crop_name}_augmentation.png', 
                dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("=" * 60)
    print("🌾 CROPSAFE DATA PREPARATION")
    print("=" * 60)
    
    # Visualize augmentation for both crops
    visualize_augmentation(WHEAT_PATH, 'wheat')
    visualize_augmentation(RICE_PATH, 'rice')
    
    # Create generators for both crops
    wheat_train, wheat_val, wheat_classes = create_data_generators(WHEAT_PATH, 'wheat')
    rice_train, rice_val, rice_classes = create_data_generators(RICE_PATH, 'rice')
    
    print("\n" + "=" * 60)
    print("✅ DATA PREPARATION COMPLETE")
    print("=" * 60)
    print("\nNext step: Train the models!")
    print("Run: python scripts/train_model.py")