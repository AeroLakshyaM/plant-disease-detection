# quick_train.py
"""
Quick training script for demo purposes
Trains a smaller model faster (3-5 minutes)
For production, use train_model_sklearn.py
"""

import numpy as np
import os
import json
import pickle
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# Configuration - REDUCED FOR SPEED
IMG_SIZE = 64  # Smaller images
TRAIN_DIR = 'dataset/train'
VAL_DIR = 'dataset/val'
MODEL_SAVE_PATH = 'plant_disease_model_sklearn.pkl'
CLASS_NAMES_PATH = 'class_names.json'
MAX_SAMPLES = 100  # Only 100 samples per class for demo

print("=" * 70)
print("Quick Training - Plant Disease Detection (Demo Mode)")
print("=" * 70)
print("\nThis will train a small model in 3-5 minutes for testing.")
print("For production, use: python train_model_sklearn.py")
print()

# Check dataset
if not os.path.exists(TRAIN_DIR):
    print("Error: Dataset not found! Run: python venv\\Split_dataset.py")
    exit(1)

# Get class names
class_names = sorted(os.listdir(TRAIN_DIR))
print(f"✓ Found {len(class_names)} disease classes")

# Save class names
with open(CLASS_NAMES_PATH, 'w') as f:
    json.dump(class_names, f, indent=2)
print(f"✓ Class names saved")

print("\nLoading training data (quick mode)...")
X_train = []
y_train = []

for idx, class_name in enumerate(class_names):
    class_path = os.path.join(TRAIN_DIR, class_name)
    if not os.path.isdir(class_path):
        continue
    
    files = [f for f in os.listdir(class_path) 
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Take only first MAX_SAMPLES
    files = files[:MAX_SAMPLES]
    
    for i, filename in enumerate(files):
        try:
            img_path = os.path.join(class_path, filename)
            img = Image.open(img_path).convert('RGB').resize((IMG_SIZE, IMG_SIZE))
            img_array = np.array(img).flatten() / 255.0
            X_train.append(img_array)
            y_train.append(idx)
        except:
            continue
    
    print(f"  {idx+1}/{len(class_names)}: {class_name[:40]}...", end='\r')

X_train = np.array(X_train)
y_train = np.array(y_train)

print(f"\n\n✓ Loaded {len(X_train)} training samples")

print("\nTraining model... (this will take 3-5 minutes)")
model = RandomForestClassifier(
    n_estimators=50,  # Fewer trees for speed
    max_depth=20,
    n_jobs=-1,
    random_state=42,
    verbose=1
)

model.fit(X_train, y_train)

print("\n✓ Training complete!")

# Save model
with open(MODEL_SAVE_PATH, 'wb') as f:
    pickle.dump(model, f)

print(f"✓ Model saved as '{MODEL_SAVE_PATH}'")

# Test accuracy
train_acc = model.score(X_train, y_train)
print(f"✓ Training accuracy: {train_acc*100:.1f}%")

print("\n" + "=" * 70)
print("Quick training complete! ✓")
print("=" * 70)
print("\nYour model is ready for the web app!")
print("\nStart the web server:")
print("  python app.py")
print("\nThen open: http://localhost:5000")
print()
