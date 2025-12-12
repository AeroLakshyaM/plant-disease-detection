# train_model_sklearn.py
"""
Plant Disease Detection Model Training Script (Scikit-learn version)
Uses Random Forest for classification - works with Python 3.14+
Lower accuracy than CNN but doesn't require TensorFlow
"""

import numpy as np
import os
import json
import pickle
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Configuration
IMG_SIZE = 128  # Smaller for faster processing
TRAIN_DIR = 'dataset/train'
VAL_DIR = 'dataset/val'
MODEL_SAVE_PATH = 'plant_disease_model_sklearn.pkl'
CLASS_NAMES_PATH = 'class_names.json'
MAX_SAMPLES_PER_CLASS = 500  # Limit for faster training

def load_images_from_folder(folder, max_samples=None):
    """Load images and labels from folder structure"""
    images = []
    labels = []
    class_names = sorted(os.listdir(folder))
    
    print(f"Loading data from {folder}...")
    
    for idx, class_name in enumerate(class_names):
        class_path = os.path.join(folder, class_name)
        if not os.path.isdir(class_path):
            continue
        
        files = [f for f in os.listdir(class_path) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Limit samples per class for faster training
        if max_samples and len(files) > max_samples:
            files = files[:max_samples]
        
        for i, filename in enumerate(files):
            try:
                img_path = os.path.join(class_path, filename)
                img = Image.open(img_path)
                
                # Convert to RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize
                img = img.resize((IMG_SIZE, IMG_SIZE))
                
                # Convert to array and flatten
                img_array = np.array(img).flatten()
                
                images.append(img_array)
                labels.append(idx)
                
                if (i + 1) % 100 == 0:
                    print(f"  {class_name}: {i+1}/{len(files)} images loaded", end='\r')
            
            except Exception as e:
                print(f"  Error loading {filename}: {e}")
                continue
        
        print(f"  ✓ {class_name}: {len([l for l in labels if l == idx])} images loaded")
    
    return np.array(images), np.array(labels), class_names

def main():
    print("=" * 70)
    print("Plant Disease Detection - Model Training (Scikit-learn)")
    print("=" * 70)
    
    # Check if dataset exists
    if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
        print("\nError: Dataset not found!")
        print("Please run 'python venv/Split_dataset.py' first.")
        return
    
    # Load training data
    print("\n[1/5] Loading training data...")
    print("-" * 70)
    X_train, y_train, class_names = load_images_from_folder(
        TRAIN_DIR, 
        max_samples=MAX_SAMPLES_PER_CLASS
    )
    
    print(f"\n✓ Training samples: {len(X_train)}")
    print(f"✓ Number of classes: {len(class_names)}")
    print(f"✓ Feature dimensions: {X_train.shape[1]}")
    
    # Load validation data
    print("\n[2/5] Loading validation data...")
    print("-" * 70)
    X_val, y_val, _ = load_images_from_folder(VAL_DIR, max_samples=200)
    
    print(f"\n✓ Validation samples: {len(X_val)}")
    
    # Save class names
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"✓ Class names saved to '{CLASS_NAMES_PATH}'")
    
    # Normalize data
    print("\n[3/5] Normalizing data...")
    X_train = X_train / 255.0
    X_val = X_val / 255.0
    print("✓ Data normalized")
    
    # Create and train model
    print("\n[4/5] Training Random Forest model...")
    print("-" * 70)
    print("This may take 10-20 minutes depending on your CPU...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1,  # Use all CPU cores
        random_state=42,
        verbose=2
    )
    
    model.fit(X_train, y_train)
    print("\n✓ Training completed!")
    
    # Evaluate model
    print("\n[5/5] Evaluating model...")
    print("-" * 70)
    
    # Training accuracy
    train_pred = model.predict(X_train)
    train_acc = accuracy_score(y_train, train_pred)
    print(f"Training Accuracy: {train_acc*100:.2f}%")
    
    # Validation accuracy
    val_pred = model.predict(X_val)
    val_acc = accuracy_score(y_val, val_pred)
    print(f"Validation Accuracy: {val_acc*100:.2f}%")
    
    # Save model
    with open(MODEL_SAVE_PATH, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✓ Model saved as '{MODEL_SAVE_PATH}'")
    
    # Summary
    print("\n" + "=" * 70)
    print("Training completed successfully!")
    print("=" * 70)
    
    print("\nModel Performance:")
    print(f"  • Training Accuracy: {train_acc*100:.2f}%")
    print(f"  • Validation Accuracy: {val_acc*100:.2f}%")
    print(f"  • Number of Classes: {len(class_names)}")
    print(f"  • Model Size: {os.path.getsize(MODEL_SAVE_PATH) / (1024*1024):.1f} MB")
    
    print("\nTo make predictions, run:")
    print("  python predict_sklearn.py path/to/image.jpg")
    
    # Display sample classes
    print("\nSample plant disease classes:")
    for i, cls in enumerate(class_names[:10]):
        print(f"  {i+1}. {cls}")
    if len(class_names) > 10:
        print(f"  ... and {len(class_names) - 10} more classes")

if __name__ == "__main__":
    main()
