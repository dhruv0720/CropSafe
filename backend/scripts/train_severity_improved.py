"""
FIX OVERFITTING - More regularization
"""
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Stronger augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    validation_split=0.2
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Load data
dataset_path = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\severity_dataset_auto"

train_gen = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_gen = val_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Model with MORE DROPOUT
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224,224,3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dropout(0.7),  # Increased from 0.5
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.7),  # Increased from 0.5
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(4, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train with early stopping
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=50,
    callbacks=[EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)],
    verbose=1
)

model.save('severity_model_fixed.h5')
print(f"Final validation accuracy: {max(history.history['val_accuracy']):.2%}")