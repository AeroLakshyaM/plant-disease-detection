<<<<<<< HEAD
# 🌱 Plant Disease Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-1.8.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**AI-powered web application to detect and classify plant diseases from leaf images**

[Live Demo](#) • [Documentation](#documentation) • [Features](#features) • [Getting Started](#getting-started)

</div>

---

## 📋 Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line](#command-line)
- [Dataset](#dataset)
- [Model Information](#model-information)
- [Deployment](#deployment)
- [GitHub Setup](#github-setup)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🌐 **Web Interface**: Beautiful, responsive web app for easy disease detection
- 🤖 **AI-Powered**: Machine learning model trained on 54,000+ plant images
- 🎯 **38 Disease Classes**: Detects diseases across multiple plant species (Apple, Tomato, Potato, Corn, Grape, etc.)
- 📱 **Mobile Friendly**: Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Fast Predictions**: Get results in 1-3 seconds
- 📊 **Confidence Scores**: See top 3 predictions with confidence percentages
- 🚀 **Easy Deployment**: Ready to deploy on Render, Railway, Heroku, or PythonAnywhere
- 💻 **CLI Support**: Command-line interface for batch processing

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10 or higher** (3.11-3.14 recommended)
- **pip** (Python package installer)
- **Git** (for version control)
- **4GB RAM minimum** (8GB recommended)
- **5GB free disk space**

### Installation

#### Step 1: Clone or Download the Repository

**Option A: Clone with Git (Recommended)**
```bash
git clone https://github.com/YOUR_USERNAME/plant-disease-detection.git
cd plant-disease-detection
```

**Option B: Download ZIP**
- Download the project as ZIP
- Extract to a folder
- Open terminal in that folder

#### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Scikit-learn (machine learning)
- NumPy (numerical computing)
- Pillow (image processing)
- Matplotlib (visualization)

#### Step 4: Prepare Dataset (If not already done)

```bash
python venv/Split_dataset.py
```

This creates train/val split from the raw dataset (80/20 split).

### Quick Start

#### Option 1: One-Click Start (Windows)

```powershell
.\run_web_app.bat
```

This will:
- Check if model exists
- Train model if needed (5 minutes)
- Start the web server
- Open at http://localhost:5000

#### Option 2: Manual Start

**Step 1: Train the Model**
```bash
# Q📂 Project Structure

```
plant-disease-detection/
│
├── 📁 plant_raw/                    # Original dataset (54K images)
│   ├── color/                       # Color images by disease
│   ├── grayscale/                   # Grayscale versions
│   └── segmented/                   # Segmented versions
│
├── 📁 dataset/                      # Processed dataset (created by split script)
│   ├── train/                       # Training set (80% - 43K images)
│   └── val/                         # Validation set (20% - 11K images)
│
├── 📁 templates/                    # Web interface templates
│   └── index.html                   # Main web page
│
├── 📁 static/                       # Static assets
│   └── style.css                    # Web interface styling
│
├── 📁 venv/                         # Python virtual environment
│   └── Split_dataset.py             # Dataset preparation script
│
├── 📄 app.py                        # Flask web application ⭐
├── 📄 train_model_sklearn.py        # ML model training (production)
├── 📄 quick_train.py                # Fast training for demo
├── 📄 train_model.py                # TensorFlow training (optional)
├── 📄 predict_sklearn.py            # CLI prediction script
├── 📄 predict.py                    # TensorFlow prediction (optional)
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 Procfile                      # For Heroku/Render deployment
├── 📄 run_web_app.bat              # Windows quick start script
│
├── 📄 README.md                     # This file
├── 📄 WEB_APP_README.md            # Web app documentation
├── 📄 DEPLOYMENT_GUIDE.md          # Deployment instructions
├── 📄 COMPLETE_GUIDE.md            # Comprehensive guide
├── 📄 PROJECT_SUMMARY.md           # Technical overview
│
└── 🔧 Generated files (after training):
    ├── plant_disease_model_sklearn.pkl  # Trained model
    ├── class_names.json                 # Disease class names
    └── training_history.png             # Training visualization
```

### Key Files Explained

| File | Purpose | When to Use |
|------|---------|-------------|
| `app.py` | Web server | Always (for web interface) |
| `quick_train.py` | Fast model training | Testing, demos |
| `train_model_sklearn.py` | Full model training | Production deployment |
| `predict_sklearn.py` | CLI predictions | Batch processing, automation |
| `run_web_app.bat` | One-click startup | Windows users |
| `requirements.txt` | Dependencies list | Installation, deployment |

---

## 🔌 API Documentation

### REST API Endpoints

#### GET `/`
Main web interface

**Response:** HTML page

---

#### POST `/predict`
Upload image and get disease prediction

**Request:**
```http
POST /predict HTTP/1.1
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "plant": "Tomato",
      "disease": "Late blight",
      "confidence": 87.34,
      "full_name": "Tomato___Late_blight"
    },
    {
      "plant": "Tomato",
      "disease": "Early blight",
      "confidence": 8.12,
      "full_name": "Tomato___Early_blight"
    },
    {
      "plant": "Potato",
      "disease": "Late blight",
      "confidence": 2.54,
      "full_name": "Potato___Late_blight"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "No file uploaded"
}
```

---

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "classes": 38
}
```

### Using the API

**cURL Example:**
```bash
curl -X POST -F "file=@plant_image.jpg" http://localhost:5000/predict
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/predict"
files = {"file": open("plant_image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => console.log(data.predictions));
```

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file for production:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PORT=5000
MAX_CONTENT_LENGTH=16777216
MODEL_PATH=plant_disease_model_sklearn.pkl
```

### Customize Settings

Edit `app.py` to change:

```python
# Image size (must match training)
IMG_SIZE = 64  # or 128, 224

# Upload settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
```

---

## 🧪 Testing

### Test the Web Interface

1. Start the server:
   ```bash
   python app.py
   ```

2. Open http://localhost:5000

3. Upload a test image from:
   ```
   dataset/val/Tomato___Late_blight/[any_image].JPG
   ```

4. Verify prediction appears

### Test the API

```bash
# Health check
curl http://localhost:5000/health

# Prediction
curl -X POST -F "file=@test_image.jpg" http://localhost:5000/predict
```

### Test CLI Tool

```bash
python predict_sklearn.py "dataset/val/Tomato___Late_blight/test.jpg"
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Model not found**
```bash
python quick_train.py
```

**2. Port already in use**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**3. Image size mismatch**
- Make sure `IMG_SIZE` in `app.py` matches training
- Default: 64 for quick_train, 128 for full training

**4. Out of memory**
- Reduce `MAX_SAMPLES_PER_CLASS` in training script
- Close other applications
- Use `quick_train.py` instead

**5. Slow predictions**
- Use smaller `IMG_SIZE` (64 instead of 128)
- Reduce `n_estimators` in RandomForest
- Use faster hosting (Railway, Render)

### Get Help

- Check [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) for detailed instructions
- Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for hosting help
- Review error messages carefully

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Ideas

- Add more plant species
- Improve model accuracy
- Add treatment recommendations
- Create mobile app
- Add multiple language support
- Improve UI/UX design

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **PlantVillage Dataset** - Training data source
- **Flask** - Web framework
- **Scikit-learn** - Machine learning library
- **TensorFlow/Keras** - Deep learning framework (optional)
- **MobileNetV2** - Transfer learning model

---

## 📞 Contact & Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the documentation files
- **Contributions**: Pull requests welcome!

---

## 🎯 Roadmap

- [x] Basic disease detection
- [x] Web interface
- [x] Multiple model options
- [x] Deployment guides
- [ ] Mobile app (React Native)
- [ ] Treatment recommendations
- [ ] Multi-language support
- [ ] Expert consultation feature
- [ ] Community forum

---

## 📈 Project Stats

- **Lines of Code**: ~2,000
- **Languages**: Python, HTML, CSS, JavaScript
- **Dependencies**: 7 main packages
- **Dataset Size**: 54,305 images
- **Model Accuracy**: Up to 98% (TensorFlow)
- **Prediction Time**: 1-3 seconds
- **Supported Diseases**: 38 classes

---

<div align="center">

**Made with ❤️ for Agriculture Technology**

[⬆ Back to Top](#-plant-disease-detection-system)

**Star ⭐ this repository if you find it helpful!**

</div>**Open browser:** http://localhost:5000

3. **Upload an image:**
   - Click the upload area or drag & drop a plant leaf image
   - Supported formats: JPG, PNG, GIF, BMP
   - Max size: 16MB

4. **Get prediction:**
   - Click "Analyze Plant"
   - View results with confidence scores
   - See top 3 possible diseases

**Example:**
```
#1 Prediction:
   Plant: Tomato
   Condition: Late blight
   Confidence: 87.34%
```

### Command Line

**Single Image:**
```bash
python predict_sklearn.py path/to/image.jpg
```

**Batch Processing:**
```bash
python predict_sklearn.py path/to/folder/
```

**Example:**
```bash
python predict_sklearn.py "dataset/val/Tomato___Late_blight/test_image.jpg"
```

---

## 📊 Dataset

The project uses the **PlantVillage Dataset**:

- **Total Images**: 54,305 leaf images
- **Training Set**: 43,429 images (80%)
- **Validation Set**: 10,876 images (20%)
- **Classes**: 38 plant disease categories
- **Location**: `plant_raw/color/` directory
- **Format**: RGB color images
- **Quality**: High-resolution plant leaf photos

### Detected Plant Diseases

| Plant | Diseases Detected |
|-------|------------------|
| 🍎 **Apple** | Apple scab, Black rot, Cedar apple rust, Healthy |
| 🍅 **Tomato** | Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Mosaic virus, Yellow Leaf Curl Virus, Healthy |
| 🥔 **Potato** | Early blight, Late blight, Healthy |
| 🌽 **Corn** | Cercospora leaf spot, Common rust, Northern Leaf Blight, Healthy |
| 🍇 **Grape** | Black rot, Esca, Leaf blight, Healthy |
| 🍑 **Peach** | Bacterial spot, Healthy |
| 🌶️ **Pepper** | Bacterial spot, Healthy |
| 🍓 **Strawberry** | Leaf scorch, Healthy |
| **Others** | Cherry, Blueberry, Raspberry, Soybean, Squash, Orange |

---

## 🤖 Model Information

### Scikit-learn Model (Default)

**Architecture:** Random Forest Classifier
- **Estimators**: 50-100 trees
- **Max Depth**: 20-30 levels
- **Input Size**: 64x64 or 128x128 RGB images
- **Features**: Flattened pixel values (normalized)
- **Training Time**: 5-20 minutes
- **Accuracy**: 70-85%
- **Model Size**: 50-200MB

### TensorFlow Model (Optional - Requires Python 3.11)

**Architecture:** Transfer Learning with MobileNetV2
- **Base Model**: MobileNetV2 (pre-trained on ImageNet)
- **Custom Layers**: GlobalAveragePooling + Dense layers
- **Input Size**: 224x224 RGB images
- **Optimizer**: Adam (lr=0.0001)
- **Training Time**: 30-60 minutes
- **Accuracy**: 92-98%
- **Model Size**: ~15MB

### Model Performance

| Model | Training Time | Accuracy | Use Case |
|-------|--------------|----------|----------|
| Quick (quick_train.py) | 3-5 min | ~70% | Demo, Testing |
| Sklearn Full | 10-20 min | ~85% | Production |
| TensorFlow CNN | 30-60 min | ~95% | Best Accuracy |

---

## 🌐 Deployment

### Deploy to Render (Free - Recommended)

1. **Push to GitHub** (see [GitHub Setup](#github-setup))

2. **Create Render account** at https://render.com

3. **New Web Service:**
   - Connect your GitHub repository
   - Name: `plant-disease-detector`
   - Environment: `Python 3`
   - Build Command:
     ```bash
     pip install -r requirements.txt && python quick_train.py
     ```
   - Start Command:
     ```bash
     gunicorn app:app
     ```

4. **Deploy!** Your app will be at: `https://your-app.onrender.com`

### Deploy to Railway (Easiest)

1. **Push to GitHub**

2. **Go to** https://railway.app

3. **Click "New Project"** → Deploy from GitHub repo

4. **Select repository** → Railway auto-deploys!

5. **Add domain** in settings

### Deploy to PythonAnywhere

1. **Create account** at https://www.pythonanywhere.com

2. **Upload files** via Files tab

3. **Open Bash console:**
   ```bash
   pip install --user -r requirements.txt
   python quick_train.py
   ```

4. **Web tab** → Add new web app → Flask → Configure paths

5. **Your site:** `yourusername.pythonanywhere.com`

### Local Network Sharing (ngrok)

Share your local server temporarily:

```bash
# Start your app
python app.py

# In another terminal
ngrok http 5000
```

Share the ngrok URL (e.g., `https://abc123.ngrok.io`)

**For detailed deployment instructions**, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📦 GitHub Setup

### Initial Setup (First Time)

**1. Create GitHub Repository**

Go to https://github.com/new and create a new repository:
- Name: `plant-disease-detection`
- Description: `AI-powered plant disease detection system`
- Public or Private
- **Don't** initialize with README (we have one)

**2. Initialize Git in Your Project**

```bash
cd plant_project
git init
```

**3. Create .gitignore File**

Create a file named `.gitignore` with:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# Model files (optional - too large for GitHub)
*.pkl
*.h5

# Dataset (too large)
dataset/
plant_raw/

# Uploads
uploads/
*.jpg
*.jpeg
*.png
*.gif

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

**4. Add and Commit Files**

```bash
git add .
git commit -m "Initial commit: Plant Disease Detection System"
```

**5. Connect to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/plant-disease-detection.git
git branch -M main
git push -u origin main
```

### Regular Updates

After making changes:

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Your descriptive message here"

# Push to GitHub
git push
```

### Example Commit Messages

```bash
git commit -m "Add web interface with Flask"
git commit -m "Fix image size mismatch in prediction"
git commit -m "Update README with deployment instructions"
git commit -m "Improve model accuracy to 85%"
```

### Handling Large Files (Optional)

If you want to include the model/dataset in GitHub:

**Install Git LFS:**
```bash
git lfs install
git lfs track "*.pkl"
git lfs track "*.h5"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

### Clone Your Repository (Later)

```bash
git clone https://github.com/YOUR_USERNAME/plant-disease-detection.git
cd plant-disease-detection
pip install -r requirements.txt
python quick_train.py
python app.py
```

---

## Project Structure

```
plant_project/
│
├── plant_raw/              # Original dataset
│   └── color/             # Color images of plant diseases
│       ├── Apple___Apple_scab/
│       ├── Tomato___Late_blight/
│       └── ...
│
├── dataset/               # Split dataset (created by script)
│   ├── train/            # Training data (80%)
│   └── val/              # Validation data (20%)
│
├── venv/
│   └── Split_dataset.py  # Dataset splitting script
│
├── train_model.py         # Model training script
├── predict.py             # Prediction/inference script
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── plant_disease_model.h5    # Trained model (generated)
├── class_names.json          # Class labels (generated)
└── training_history.png      # Training plots (generated)
```

## Detected Plant Diseases

The system can detect the following conditions:

**Apple:** Apple scab, Black rot, Cedar apple rust, Healthy

**Tomato:** Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Mosaic virus, Yellow Leaf Curl Virus, Healthy

**Potato:** Early blight, Late blight, Healthy

**Corn:** Cercospora leaf spot, Common rust, Northern Leaf Blight, Healthy

**Grape:** Black rot, Esca, Leaf blight, Healthy

**And more:** Peach, Pepper, Strawberry, Cherry, Blueberry, Raspberry, Soybean, Squash, Orange

## Model Architecture

- **Base Model:** MobileNetV2 (pre-trained on ImageNet)
- **Custom Layers:** Global pooling → Dense(256) → Dense(38)
- **Activation:** ReLU for hidden layers, Softmax for output
- **Optimizer:** Adam with learning rate 0.0001
- **Loss Function:** Categorical crossentropy
- **Regularization:** Dropout (0.2, 0.3)

## Performance Tips

1. **Use clear, well-lit images** of plant leaves
2. **Focus on the affected area** of the leaf
3. **Avoid blurry images** for better accuracy
4. **RGB images work best** (224x224 will be used internally)

## Troubleshooting

**Error: Dataset not found**
- Run `python venv/Split_dataset.py` first to prepare the data

**Low accuracy during training**
- Increase EPOCHS in train_model.py
- Try unfreezing some base model layers for fine-tuning

**Out of memory**
- Reduce BATCH_SIZE in train_model.py
- Use a machine with more RAM/GPU memory

## Future Improvements

- [ ] Web interface for easy image upload
- [ ] Mobile app deployment
- [ ] Real-time disease detection from camera
- [ ] Treatment recommendations
- [ ] Support for more plant species

## License

This project is for educational purposes. Dataset credit: PlantVillage Dataset.

---

**Need help?** Check that all dependencies are installed and the dataset is properly prepared.
=======
# plant-disease-detection
>>>>>>> 0291fb9b8548d1ff25d5f4c14e7acfc427eccbbe
