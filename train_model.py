# train_model.py
"""
Plant Disease Detection Model Training Script
Uses CNN architecture with data augmentation
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os
import json

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 0.0001

TRAIN_DIR = 'dataset/train'
VAL_DIR = 'dataset/val'
MODEL_SAVE_PATH = 'plant_disease_model.h5'
CLASS_NAMES_PATH = 'class_names.json'

def create_model(num_classes):
    """Create CNN model with transfer learning using MobileNetV2"""
    
    # Load pre-trained MobileNetV2 without top layers
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Build model
    model = keras.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.Rescaling(1./127.5, offset=-1),  # Normalize to [-1, 1]
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def prepare_data():
    """Prepare data generators with augmentation"""
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        shear_range=0.15,
        fill_mode='nearest'
    )
    
    # Validation data (no augmentation)
    val_datagen = ImageDataGenerator()
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator

def plot_training_history(history):
    """Plot training and validation accuracy/loss"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    print("\nTraining history plot saved as 'training_history.png'")
    plt.show()

def main():
    print("=" * 60)
    print("Plant Disease Detection - Model Training")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
        print("\nError: Dataset not found!")
        print("Please run 'python venv/Split_dataset.py' first to create the dataset.")
        return
    
    # Prepare data
    print("\n[1/5] Loading and preparing data...")
    train_gen, val_gen = prepare_data()
    
    num_classes = len(train_gen.class_indices)
    class_names = list(train_gen.class_indices.keys())
    
    print(f"   ✓ Found {num_classes} classes")
    print(f"   ✓ Training samples: {train_gen.samples}")
    print(f"   ✓ Validation samples: {val_gen.samples}")
    
    # Save class names for inference
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"   ✓ Class names saved to '{CLASS_NAMES_PATH}'")
    
    # Create model
    print(f"\n[2/5] Building model...")
    model = create_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"   ✓ Model created with {model.count_params():,} parameters")
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    print(f"\n[3/5] Training model for {EPOCHS} epochs...")
    print("-" * 60)
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate model
    print("\n[4/5] Evaluating model...")
    val_loss, val_accuracy = model.evaluate(val_gen, verbose=0)
    print(f"   ✓ Validation Accuracy: {val_accuracy*100:.2f}%")
    print(f"   ✓ Validation Loss: {val_loss:.4f}")
    
    # Plot results
    print("\n[5/5] Generating training plots...")
    plot_training_history(history)
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Model saved as '{MODEL_SAVE_PATH}'")
    print("=" * 60)
    
    # Display sample classes
    print("\nSome of the plant disease classes:")
    for i, cls in enumerate(class_names[:10]):
        print(f"  {i+1}. {cls}")
    if len(class_names) > 10:
        print(f"  ... and {len(class_names) - 10} more classes")

if __name__ == "__main__":
    main()
