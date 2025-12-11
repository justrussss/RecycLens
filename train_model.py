"""
Example script for dataset preprocessing and model training.
This demonstrates how to prepare data for training your plastic classifier model.
"""

import os
import cv2
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from sklearn.train_test_split import train_test_split

# Configuration
DATASET_PATH = 'datasets/'
TARGET_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
VALIDATION_SPLIT = 0.2

# Plastic type labels
PLASTIC_TYPES = ['PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'Other']


def load_and_preprocess_images(dataset_path, target_size=TARGET_SIZE):
    """
    Load and preprocess images from the dataset directory.
    
    Expected directory structure:
    datasets/
    ├── PET/
    │   ├── image1.jpg
    │   └── image2.jpg
    ├── HDPE/
    ├── PVC/
    ... etc
    """
    images = []
    labels = []
    
    for label_idx, plastic_type in enumerate(PLASTIC_TYPES):
        plastic_dir = os.path.join(dataset_path, plastic_type)
        
        if not os.path.exists(plastic_dir):
            print(f"Warning: {plastic_dir} not found. Skipping...")
            continue
        
        print(f"Loading {plastic_type} images...")
        
        for img_file in os.listdir(plastic_dir):
            img_path = os.path.join(plastic_dir, img_file)
            
            try:
                # Load image
                img = cv2.imread(img_path)
                if img is None:
                    continue
                
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize to target size
                img = cv2.resize(img, target_size)
                
                # Normalize to [0, 1]
                img = img / 255.0
                
                images.append(img)
                labels.append(label_idx)
                
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
                continue
    
    return np.array(images), np.array(labels)


def create_data_augmentation():
    """
    Create data augmentation pipeline for training.
    This improves model robustness by augmenting training data.
    """
    return keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.2),
        keras.layers.RandomZoom(0.2),
        keras.layers.RandomTranslation(0.1, 0.1),
        keras.layers.RandomBrightness(0.2),
        keras.layers.RandomContrast(0.2),
    ], name="data_augmentation")


def build_model(input_shape=(224, 224, 3), num_classes=7, use_pretrained=True):
    """
    Build a CNN model for plastic classification.
    
    Args:
        input_shape: Input image shape
        num_classes: Number of plastic type classes
        use_pretrained: Whether to use MobileNetV2 transfer learning
    
    Returns:
        Compiled Keras model
    """
    
    if use_pretrained:
        # Transfer learning with MobileNetV2
        base_model = keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        model = keras.Sequential([
            # Data augmentation
            create_data_augmentation(),
            
            # Preprocessing for MobileNetV2
            keras.layers.Rescaling(1./127.5, offset=-1),
            
            # Base model
            base_model,
            
            # Custom top layers
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        
    else:
        # Simple CNN from scratch
        model = keras.Sequential([
            # Data augmentation
            create_data_augmentation(),
            
            # Normalization
            keras.layers.Rescaling(1./255),
            
            # Convolutional blocks
            keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            
            keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            
            keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            
            # Flattening and Dense layers
            keras.layers.Flatten(),
            keras.layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
    
    return model


def train_model(model, train_images, train_labels, val_images, val_labels):
    """
    Train the model with callbacks.
    
    Args:
        model: Keras model to train
        train_images: Training images
        train_labels: Training labels
        val_images: Validation images
        val_labels: Validation labels
    """
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            'models/plastic_classifier_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        train_images, train_labels,
        validation_data=(val_images, val_labels),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    return history


def evaluate_model(model, test_images, test_labels):
    """Evaluate model on test set."""
    test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    return test_accuracy


def main():
    """Main training script."""
    
    print("=" * 50)
    print("RecycLens - Plastic Classifier Training")
    print("=" * 50)
    
    # 1. Load and preprocess data
    print("\n1. Loading and preprocessing images...")
    images, labels = load_and_preprocess_images(DATASET_PATH)
    
    if len(images) == 0:
        print("\nError: No images found. Please ensure dataset is in the correct format:")
        print(f"  {DATASET_PATH}")
        print(f"  ├── PET/")
        print(f"  ├── HDPE/")
        print(f"  ├── etc...")
        return
    
    print(f"Loaded {len(images)} images")
    print(f"Shape: {images.shape}")
    print(f"Labels: {np.bincount(labels)}")
    
    # 2. Split data
    print("\n2. Splitting data into train/val/test...")
    train_images, temp_images, train_labels, temp_labels = train_test_split(
        images, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    val_images, test_images, val_labels, test_labels = train_test_split(
        temp_images, temp_labels, test_size=0.5, random_state=42, stratify=temp_labels
    )
    
    print(f"Training: {len(train_images)} | Validation: {len(val_images)} | Test: {len(test_images)}")
    
    # 3. Build model
    print("\n3. Building model...")
    model = build_model(use_pretrained=True)
    print(f"Model created with {model.count_params():,} parameters")
    
    # 4. Train model
    print("\n4. Training model...")
    history = train_model(model, train_images, train_labels, val_images, val_labels)
    
    # 5. Evaluate model
    print("\n5. Evaluating model...")
    accuracy = evaluate_model(model, test_images, test_labels)
    
    # 6. Save model
    print("\n6. Saving model...")
    model.save('models/plastic_classifier.h5')
    print("Model saved to models/plastic_classifier.h5")
    
    # 7. Convert to TFLite for mobile deployment (optional)
    print("\n7. Converting to TensorFlow Lite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    with open('models/plastic_classifier.tflite', 'wb') as f:
        f.write(tflite_model)
    print("Model saved to models/plastic_classifier.tflite")
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)
    print(f"\nTo use the trained model:")
    print("1. Ensure models/plastic_classifier.h5 is in the models directory")
    print("2. Update models/classifier.py to load your trained model")
    print("3. Run: python app.py")


if __name__ == '__main__':
    main()
