"""
Plant Disease Detection - Streamlit App
Simple and beautiful web interface using Streamlit
"""

import streamlit as st
import pickle
import json
import numpy as np
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
MODEL_PATH = 'plant_disease_model_sklearn.pkl'
CLASS_NAMES_PATH = 'class_names.json'
IMG_SIZE = 64

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: transparent;
    }
    h1 {
        color: white;
        text-align: center;
    }
    .uploadedFile {
        border: 2px solid #10b981;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load model and class names"""
    try:
        if not os.path.exists(MODEL_PATH):
            return None, None, "Model not found! Please train the model first."
        
        if not os.path.exists(CLASS_NAMES_PATH):
            return None, None, "Class names not found!"
        
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
        
        return model, class_names, None
    
    except Exception as e:
        return None, None, f"Error loading model: {str(e)}"

def preprocess_image(image):
    """Preprocess image for prediction"""
    try:
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize
        image = image.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to array and flatten
        img_array = np.array(image).flatten()
        
        # Normalize
        img_array = img_array / 255.0
        
        # Reshape for prediction
        img_array = img_array.reshape(1, -1)
        
        return img_array
    
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def predict_disease(model, class_names, image):
    """Predict disease from image"""
    try:
        # Preprocess
        img_array = preprocess_image(image)
        
        if img_array is None:
            return None
        
        # Make prediction
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
                'confidence': confidence
            })
        
        return results
    
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# Main app
def main():
    # Title
    st.markdown("<h1>🌱 Plant Disease Detection</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Upload a plant leaf image to detect diseases using AI</p>", unsafe_allow_html=True)
    
    # Load model
    model, class_names, error = load_model()
    
    if error:
        st.error(error)
        st.info("Train the model first by running: `python quick_train.py`")
        return
    
    st.success(f"✓ Model loaded successfully! Recognizes {len(class_names)} disease classes")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        🌾 **Plant Disease Detection System**
        
        This AI-powered tool can detect:
        - 38 different plant diseases
        - Multiple plant species
        - Healthy vs diseased plants
        
        **Supported Plants:**
        🍎 Apple • 🍅 Tomato • 🥔 Potato
        🌽 Corn • 🍇 Grape • 🍑 Peach
        🌶️ Pepper • 🍓 Strawberry & more!
        """)
        
        st.header("How to Use")
        st.markdown("""
        1. Upload a clear plant leaf image
        2. Wait for analysis
        3. View predictions with confidence scores
        """)
        
        st.header("Tips for Best Results")
        st.markdown("""
        - Use clear, well-lit photos
        - Focus on the affected area
        - Avoid blurry images
        - RGB color images work best
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a plant leaf image",
            type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            help="Supported formats: JPG, PNG, GIF, BMP"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Plant Disease", type="primary", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    results = predict_disease(model, class_names, image)
                    
                    if results:
                        st.session_state['results'] = results
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if 'results' in st.session_state and st.session_state['results']:
            results = st.session_state['results']
            
            for i, result in enumerate(results, 1):
                confidence = result['confidence']
                
                # Determine color based on confidence
                if confidence > 50:
                    color = "#10b981"  # Green
                    level = "High"
                elif confidence > 25:
                    color = "#f59e0b"  # Yellow
                    level = "Medium"
                else:
                    color = "#ef4444"  # Red
                    level = "Low"
                
                # Display result card
                st.markdown(f"""
                <div style='background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid {color};'>
                    <h3 style='color: {color}; margin: 0;'>#{i} Prediction</h3>
                    <p style='margin: 5px 0;'><strong>Plant:</strong> {result['plant']}</p>
                    <p style='margin: 5px 0;'><strong>Condition:</strong> {result['disease']}</p>
                    <p style='margin: 5px 0;'><strong>Confidence:</strong> {confidence:.2f}% ({level})</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation
            top_result = results[0]
            if top_result['confidence'] > 60:
                st.success(f"✅ High confidence: {top_result['plant']} - {top_result['disease']}")
            elif top_result['confidence'] > 30:
                st.info(f"ℹ️ Moderate confidence: {top_result['plant']} - {top_result['disease']}")
            else:
                st.warning(f"⚠️ Lower confidence: Consider uploading a clearer, well-lit image")
        
        else:
            st.info("👆 Upload an image and click 'Analyze' to see results")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white;'>
        <p>Made with ❤️ for Agriculture Technology</p>
        <p>Powered by Machine Learning & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
