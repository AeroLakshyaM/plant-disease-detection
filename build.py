"""
Render/Railway Build Script
Run this during deployment to train the model
"""
import os
import sys

print("=" * 70)
print("Deployment Build - Training Model")
print("=" * 70)

# Check if model already exists
if os.path.exists('plant_disease_model_sklearn.pkl'):
    print("Model already exists - skipping training")
    sys.exit(0)

# Check if dataset exists
if not os.path.exists('dataset/train'):
    print("ERROR: Dataset not found!")
    print("The dataset is too large for GitHub.")
    print("For production, upload dataset separately or use cloud storage.")
    sys.exit(1)

# Train the model
print("\nTraining model for production...")
import subprocess
result = subprocess.run([sys.executable, 'quick_train.py'], capture_output=True, text=True)
print(result.stdout)

if result.returncode == 0:
    print("\n✓ Model trained successfully!")
else:
    print("\n✗ Model training failed!")
    print(result.stderr)
    sys.exit(1)
