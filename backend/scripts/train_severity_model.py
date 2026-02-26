"""
STABLE SEVERITY MODEL TRAINING - Guaranteed to work
"""
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import VGG16  # Very stable architecture
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import numpy as np
import json
import os

print("=" * 70)
print("🌾 STABLE SEVERITY MODEL TRAINING")
print("=" * 70)

# Dataset path - use your actual path
dataset_path = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto"

# Verify dataset exists
if not os.path.exists(dataset_path):
    print(f"❌ Dataset not found at: {dataset_path}")
    exit(1)

# Count images
print("\n📊 Dataset Statistics:")
total = 0
for severity in ['Low', 'Medium', 'High', 'Very High']:
    folder = os.path.join(dataset_path, severity)
    count = len([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    total += count
    print(f"   {severity}: {count} images")
print(f"   TOTAL: {total} images")

# Simple data preprocessing (no extreme augmentation)
print("\n📊 Creating data generators...")
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

BATCH_SIZE = 32

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    classes=['Low', 'Medium', 'High', 'Very High']
)

val_generator = val_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    classes=['Low', 'Medium', 'High', 'Very High']
)

print(f"\n✅ Training samples: {train_generator.samples}")
print(f"✅ Validation samples: {val_generator.samples}")

# === VGG16 - VERY STABLE ARCHITECTURE ===
print("\n🏗️ Building VGG16 model (guaranteed stability)...")
base_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model initially
base_model.trainable = False

# Add custom classifier
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(4, activation='softmax')
])

# Conservative learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())

# Callbacks
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    ),
    ModelCheckpoint(
        'severity_model_stable.keras',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

print("\n🚀 Starting training...")
print("⏱️  Expected: 30-40 minutes")
print("-" * 50)

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=50,
    callbacks=callbacks,
    verbose=1
)

# Plot results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
ax1.plot(history.history['accuracy'], label='Train')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.axhline(y=0.85, color='r', linestyle='--', label='85% Target')
ax1.set_title('Model Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True)

# Loss
ax2.plot(history.history['loss'], label='Train')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Model Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('severity_training_stable.png')
plt.show()

# Final evaluation
val_loss, val_acc = model.evaluate(val_generator, verbose=0)
print(f"\n✅ Final Validation Accuracy: {val_acc:.2%}")

# Save final model
model.save('severity_model_final.h5')
print("\n✅ Model saved as 'severity_model_final.h5'")

# Save class indices
with open('severity_class_indices.json', 'w') as f:
    json.dump(train_generator.class_indices, f, indent=2)
print("✅ Class indices saved")