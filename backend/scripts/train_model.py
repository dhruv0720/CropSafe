"""
Train CNN models for wheat and rice disease detection
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

# Import the data generators from prepare_data
from prepare_data import create_data_generators
import prepare_data

class DiseaseClassifier:
    def __init__(self, crop_name, num_classes, img_size=(224, 224)):
        self.crop_name = crop_name
        self.num_classes = num_classes
        self.img_size = img_size
        self.model = None
        self.history = None
        
    def build_model(self):
        """Build transfer learning model with MobileNetV2"""
        print(f"\n🏗️  Building model for {self.crop_name}...")
        
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.img_size, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification head
        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        print(f"✅ Model built for {self.crop_name}")
        print(self.model.summary())
        
    def train(self, train_generator, val_generator, epochs=50):
        """Train the model"""
        print(f"\n🚀 Training {self.crop_name} model...")
        
        # Create callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-6,
                verbose=1
            ),
            ModelCheckpoint(
                f'../models/{self.crop_name}_best.keras',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train
        self.history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def plot_training_history(self):
        """Plot training curves"""
        if self.history is None:
            print("No training history found")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'{self.crop_name.title()} Model Training History', fontsize=16, fontweight='bold')
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Accuracy')
        axes[0, 0].set_xlabel('Epochs')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Loss')
        axes[0, 1].set_xlabel('Epochs')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        if 'precision' in self.history.history:
            axes[1, 0].plot(self.history.history['precision'], label='Train')
            axes[1, 0].plot(self.history.history['val_precision'], label='Validation')
            axes[1, 0].set_title('Precision')
            axes[1, 0].set_xlabel('Epochs')
            axes[1, 0].set_ylabel('Precision')
            axes[1, 0].legend()
            axes[1, 0].grid(True)
        
        # Recall
        if 'recall' in self.history.history:
            axes[1, 1].plot(self.history.history['recall'], label='Train')
            axes[1, 1].plot(self.history.history['val_recall'], label='Validation')
            axes[1, 1].set_title('Recall')
            axes[1, 1].set_xlabel('Epochs')
            axes[1, 1].set_ylabel('Recall')
            axes[1, 1].legend()
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(f'../models/training_history/{self.crop_name}_history.png', 
                    dpi=150, bbox_inches='tight')
        plt.show()
    
    def save_model(self):
        """Save the final model"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save in Keras format
        model_path = f'../models/{self.crop_name}_final_{timestamp}.keras'
        self.model.save(model_path)
        print(f"✅ Model saved to {model_path}")
        
        # Also save in H5 format for compatibility
        h5_path = f'../models/{self.crop_name}_model.h5'
        self.model.save(h5_path)
        print(f"✅ Model also saved as {h5_path}")
        
        # Save training history
        with open(f'../models/training_history/{self.crop_name}_history.pkl', 'wb') as f:
            pickle.dump(self.history.history, f)
        
        return model_path
    
    def evaluate(self, test_generator):
        """Evaluate model on test data"""
        print(f"\n📊 Evaluating {self.crop_name} model...")
        
        results = self.model.evaluate(test_generator)
        metrics = ['Loss', 'Accuracy', 'Precision', 'Recall']
        
        print(f"\n{'='*40}")
        print(f"Evaluation Results for {self.crop_name}")
        print(f"{'='*40}")
        for name, value in zip(metrics, results):
            print(f"{name:15}: {value:.4f}")
        
        return results

def train_crop_model(crop_path, crop_name, epochs=30):
    """Complete pipeline for training a crop model"""
    print(f"\n{'='*60}")
    print(f"🌾 TRAINING {crop_name.upper()} MODEL")
    print(f"{'='*60}")
    
    # Create data generators
    train_gen, val_gen, class_indices = create_data_generators(
        crop_path, 
        crop_name,
        img_size=(224, 224),
        batch_size=32
    )
    
    # Create and build model
    classifier = DiseaseClassifier(crop_name, len(class_indices))
    classifier.build_model()
    
    # Train model
    history = classifier.train(train_gen, val_gen, epochs=epochs)
    
    # Plot training history
    classifier.plot_training_history()
    
    # Evaluate model
    classifier.evaluate(val_gen)
    
    # Save model
    classifier.save_model()
    
    return classifier

if __name__ == "__main__":
    print("=" * 60)
    print("🌾 CROPSAFE MODEL TRAINING")
    print("=" * 60)
    
    # Paths (using the same confirmed path)
    BASE_PATH = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
    WHEAT_PATH = os.path.join(BASE_PATH, 'Wheat')
    RICE_PATH = os.path.join(BASE_PATH, 'Rice')
    
    # Train wheat model (15 classes)
    wheat_classifier = train_crop_model(WHEAT_PATH, 'wheat', epochs=30)
    
    # Train rice model (4 classes)
    rice_classifier = train_crop_model(RICE_PATH, 'rice', epochs=30)
    
    print("\n" + "=" * 60)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 60)
    print("\nModels saved in: backend/models/")
    print("Training history saved in: backend/models/training_history/")