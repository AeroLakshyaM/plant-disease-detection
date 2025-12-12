"""
Plant Disease Detection - Web Application
Simple Flask app for uploading images and detecting plant diseases
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import pickle
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import traceback

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MODEL_PATH = 'plant_disease_model_sklearn.pkl'
CLASS_NAMES_PATH = 'class_names.json'
IMG_SIZE = 64  # Must match the size used during training

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for model and classes
model = None
class_names = None

def load_model():
    """Load the trained model and class names"""
    global model, class_names
    
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            print(f"✓ Model loaded from {MODEL_PATH}")
        else:
            print(f"⚠ Model not found at {MODEL_PATH}")
            print("  Please train the model first: python train_model_sklearn.py")
            return False
        
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"✓ Class names loaded ({len(class_names)} classes)")
        else:
            print(f"⚠ Class names not found at {CLASS_NAMES_PATH}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img = img.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to array and flatten
        img_array = np.array(img).flatten()
        
        # Normalize
        img_array = img_array / 255.0
        
        # Reshape for prediction
        img_array = img_array.reshape(1, -1)
        
        return img_array
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_path):
    """Predict disease from uploaded image"""
    global model, class_names
    
    if model is None or class_names is None:
        return None, "Model not loaded"
    
    try:
        # Preprocess image
        img_array = preprocess_image(image_path)
        
        if img_array is None:
            return None, "Error processing image"
        
        # Make prediction
        prediction = model.predict(img_array)[0]
        probabilities = model.predict_proba(img_array)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        
        results = []
        for idx in top_indices:
            disease_name = class_names[idx]
            confidence = float(probabilities[idx] * 100)
            
            # Parse disease name
            parts = disease_name.split('___')
            if len(parts) == 2:
                plant = parts[0].replace('_', ' ')
                disease = parts[1].replace('_', ' ')
            else:
                plant = "Unknown"
                disease = disease_name.replace('_', ' ')
            
            results.append({
                'plant': plant,
                'disease': disease,
                'confidence': round(confidence, 2),
                'full_name': disease_name
            })
        
        return results, None
    
    except Exception as e:
        error_msg = f"Prediction error: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return None, error_msg

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', model_loaded=(model is not None))

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    
    # Check if model is loaded
    if model is None or class_names is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first using: python train_model_sklearn.py'
        })
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        })
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        })
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        })
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        results, error = predict_disease(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            })
        
        return jsonify({
            'success': True,
            'predictions': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'classes': len(class_names) if class_names else 0
    })

if __name__ == '__main__':
    print("=" * 70)
    print("Plant Disease Detection - Web Application")
    print("=" * 70)
    print()
    
    # Load model
    print("Loading model...")
    if load_model():
        print()
        print("✓ Application ready!")
        print()
        print("=" * 70)
        print("Starting server...")
        print("=" * 70)
        print()
        print("🌐 Open your browser and go to: http://localhost:5000")
        print()
        print("Press Ctrl+C to stop the server")
        print()
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print()
        print("✗ Failed to load model!")
        print()
        print("Please train the model first:")
        print("  python train_model_sklearn.py")
        print()
