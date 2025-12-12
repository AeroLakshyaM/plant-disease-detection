# setup_instructions.md

# Setup Instructions for Plant Disease Detection

## Issue: TensorFlow Compatibility

TensorFlow currently doesn't support Python 3.14. You have two options:

## Option 1: Use Python 3.11 (Recommended)

1. **Install Python 3.11** from https://www.python.org/downloads/

2. **Create a new virtual environment with Python 3.11:**
   ```powershell
   cd "C:\Users\Lakshya mishra\plant_project"
   py -3.11 -m venv venv311
   ```

3. **Activate the environment:**
   ```powershell
   .\venv311\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install tensorflow numpy matplotlib pillow
   ```

5. **Split the dataset** (if not done already):
   ```powershell
   python venv\Split_dataset.py
   ```

6. **Train the model:**
   ```powershell
   python train_model.py
   ```

7. **Make predictions:**
   ```powershell
   python predict.py path/to/image.jpg
   ```

## Option 2: Use Alternative Machine Learning Library

I can create a version using scikit-learn and traditional ML instead of deep learning, which works with Python 3.14 but may have lower accuracy.

## Quick Setup Commands (Option 1)

```powershell
# Install Python 3.11, then run:
cd "C:\Users\Lakshya mishra\plant_project"
py -3.11 -m venv venv311
.\venv311\Scripts\Activate.ps1
pip install tensorflow numpy matplotlib pillow
python train_model.py
```

## Verification

After training completes (30-60 minutes), you should see:
- `plant_disease_model.h5` - the trained model
- `class_names.json` - class labels
- `training_history.png` - training visualization

Then test with:
```powershell
python predict.py dataset/val/Tomato___Late_blight/00b89c97-5bb5-4ef4-9e43-d4f0a1a22c9a___RS_Late.B 5969.JPG
```

## Need Help?

If you can't install Python 3.11, let me know and I'll create an alternative version using scikit-learn.
