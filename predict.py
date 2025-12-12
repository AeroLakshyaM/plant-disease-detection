# predict.py
"""
Plant Disease Detection - Prediction Script
Load trained model and predict diseases from plant images
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import json
import sys
import os

# Configuration
MODEL_PATH = 'plant_disease_model.h5'
CLASS_NAMES_PATH = 'class_names.json'
IMG_SIZE = 224

def load_model_and_classes():
    """Load trained model and class names"""
    
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file '{MODEL_PATH}' not found!")
        print("Please train the model first using 'python train_model.py'")
        return None, None
    
    if not os.path.exists(CLASS_NAMES_PATH):
        print(f"Error: Class names file '{CLASS_NAMES_PATH}' not found!")
        return None, None
    
    # Load model
    model = keras.models.load_model(MODEL_PATH)
    
    # Load class names
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
    
    return model, class_names

def preprocess_image(image_path):
    """Load and preprocess image for prediction"""
    
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img = img.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to array
        img_array = np.array(img)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, img
    
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

def predict_disease(model, class_names, image_path, top_k=3):
    """Predict disease from image"""
    
    print(f"\nAnalyzing: {image_path}")
    print("-" * 60)
    
    # Preprocess image
    img_array, original_img = preprocess_image(image_path)
    
    if img_array is None:
        return
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    
    # Get top predictions
    top_indices = np.argsort(predictions[0])[-top_k:][::-1]
    
    print("\nPrediction Results:")
    print("=" * 60)
    
    for i, idx in enumerate(top_indices, 1):
        disease_name = class_names[idx]
        confidence = predictions[0][idx] * 100
        
        # Parse the disease name
        parts = disease_name.split('___')
        if len(parts) == 2:
            plant, disease = parts
            plant = plant.replace('_', ' ')
            disease = disease.replace('_', ' ')
            
            print(f"\n#{i} Prediction:")
            print(f"   Plant: {plant}")
            print(f"   Condition: {disease}")
            print(f"   Confidence: {confidence:.2f}%")
        else:
            print(f"\n#{i} {disease_name}: {confidence:.2f}%")
    
    print("\n" + "=" * 60)
    
    # Get top prediction
    top_class = class_names[top_indices[0]]
    top_confidence = predictions[0][top_indices[0]] * 100
    
    if top_confidence > 80:
        print(f"✓ High confidence prediction: {top_class}")
    elif top_confidence > 50:
        print(f"⚠ Medium confidence prediction: {top_class}")
    else:
        print(f"⚠ Low confidence - consider retaking the image")
    
    return top_class, top_confidence

def predict_batch(model, class_names, image_dir):
    """Predict diseases for all images in a directory"""
    
    if not os.path.isdir(image_dir):
        print(f"Error: '{image_dir}' is not a directory")
        return
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [f for f in os.listdir(image_dir) 
                   if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No image files found in '{image_dir}'")
        return
    
    print(f"\nFound {len(image_files)} images to process")
    print("=" * 60)
    
    results = []
    
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        result = predict_disease(model, class_names, img_path, top_k=1)
        if result:
            results.append((img_file, result[0], result[1]))
    
    # Summary
    print("\n\nBatch Processing Summary:")
    print("=" * 60)
    for img_file, disease, confidence in results:
        print(f"{img_file:30s} -> {disease:40s} ({confidence:.1f}%)")

def main():
    print("=" * 60)
    print("Plant Disease Detection - Prediction")
    print("=" * 60)
    
    # Load model and classes
    print("\nLoading model...")
    model, class_names = load_model_and_classes()
    
    if model is None or class_names is None:
        return
    
    print(f"✓ Model loaded successfully")
    print(f"✓ Recognizes {len(class_names)} plant disease classes")
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  Single image:    python predict.py <image_path>")
        print("  Batch processing: python predict.py <directory_path>")
        print("\nExample:")
        print("  python predict.py test_image.jpg")
        print("  python predict.py test_images/")
        return
    
    path = sys.argv[1]
    
    # Check if path exists
    if not os.path.exists(path):
        print(f"\nError: Path '{path}' does not exist!")
        return
    
    # Predict
    if os.path.isfile(path):
        predict_disease(model, class_names, path)
    elif os.path.isdir(path):
        predict_batch(model, class_names, path)
    else:
        print(f"Error: '{path}' is not a valid file or directory")

if __name__ == "__main__":
    main()
