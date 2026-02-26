"""
Simple retraining script with guaranteed model saving
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pickle
import sys

print("=" * 60)
print("🌾 CROPSAFE MODEL RETRAINING")
print("=" * 60)

# Force save to current directory
SAVE_DIR = os.getcwd()
print(f"📁 Models will be saved to: {SAVE_DIR}")

# Dataset path - using your confirmed path
BASE_PATH = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
WHEAT_PATH = os.path.join(BASE_PATH, 'Wheat')
RICE_PATH = os.path.join(BASE_PATH, 'Rice')

# Verify paths exist
print(f"\n🔍 Verifying dataset paths...")
print(f"Wheat path exists: {os.path.exists(WHEAT_PATH)}")
print(f"Rice path exists: {os.path.exists(RICE_PATH)}")

if not os.path.exists(WHEAT_PATH) or not os.path.exists(RICE_PATH):
    print("❌ Dataset paths not found!")
    sys.exit(1)

def train_crop_model(crop_path, crop_name, img_size=(224, 224), epochs=15):
    """Train a model for a specific crop"""
    print(f"\n{'='*50}")
    print(f"Training {crop_name.upper()} model")
    print(f"{'='*50}")
    
    # Create data generators
    print("\n📊 Creating data generators...")
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        validation_split=0.2
    )
    
    train_generator = datagen.flow_from_directory(
        crop_path,
        target_size=img_size,
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = datagen.flow_from_directory(
        crop_path,
        target_size=img_size,
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    
    print(f"\n📊 Classes found: {train_generator.class_indices}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {val_generator.samples}")
    
    # Build model
    print("\n🏗️ Building model...")
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(*img_size, 3)
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(len(train_generator.class_indices), activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(model.summary())
    
    # Train
    print(f"\n🚀 Training for {epochs} epochs...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        verbose=1
    )
    
    # Save model in current directory
    print("\n💾 Saving model...")
    
    # Save model
    model_path = os.path.join(SAVE_DIR, f'{crop_name}_model.h5')
    model.save(model_path)
    print(f"✅ Model saved to: {model_path}")
    
    # Save class indices
    indices_path = os.path.join(SAVE_DIR, f'{crop_name}_class_indices.pkl')
    with open(indices_path, 'wb') as f:
        pickle.dump(train_generator.class_indices, f)
    print(f"✅ Class indices saved to: {indices_path}")
    
    # Print final accuracy
    final_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print(f"\n📊 Final Results:")
    print(f"   Training accuracy: {final_acc:.2%}")
    print(f"   Validation accuracy: {final_val_acc:.2%}")
    
    return model, history

if __name__ == "__main__":
    print("\n✅ Paths verified, starting training...")
    
    # Train wheat model
    print("\n🌾 Training wheat model...")
    wheat_model, wheat_history = train_crop_model(WHEAT_PATH, 'wheat', epochs=15)
    
    # Train rice model
    print("\n🌾 Training rice model...")
    rice_model, rice_history = train_crop_model(RICE_PATH, 'rice', epochs=15)
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Models saved to: {SAVE_DIR}")
    print("\nFiles created:")
    print("  - wheat_model.h5")
    print("  - wheat_class_indices.pkl")
    print("  - rice_model.h5")
    print("  - rice_class_indices.pkl")
    
    # Verify files exist
    print("\n🔍 Verifying saved files:")
    for filename in ['wheat_model.h5', 'wheat_class_indices.pkl', 'rice_model.h5', 'rice_class_indices.pkl']:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / (1024*1024)  # Size in MB
            print(f"  ✅ {filename} - {size:.2f} MB")
        else:
            print(f"  ❌ {filename} - NOT FOUND")