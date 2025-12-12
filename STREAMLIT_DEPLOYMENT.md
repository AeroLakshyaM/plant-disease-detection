# 🚀 Streamlit App - Deployment Guide

## 📱 Run Locally

### Step 1: Open Terminal
```powershell
# Navigate to project folder (if not already there)
cd "C:\Users\Lakshya mishra\plant_project"
```

### Step 2: Activate Virtual Environment
```powershell
.venv\Scripts\activate
```

### Step 3: Run Streamlit App
```powershell
streamlit run streamlit_app.py
```

The app will open automatically in your browser at: **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud (FREE)

### Method 1: Deploy from GitHub (Recommended)

#### Step 1: Push to GitHub
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Add Streamlit app for plant disease detection"

# Push to GitHub
git remote add origin https://github.com/AeroLakshyaM/plant-disease-detection.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy on Streamlit Cloud

1. **Go to**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click**: "New app"

4. **Fill in**:
   - Repository: `AeroLakshyaM/plant-disease-detection`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Click**: "Deploy!"

6. **Wait** 2-3 minutes for deployment

7. **Your app will be live at**: 
   ```
   https://aerolakshyam-plant-disease-detection.streamlit.app/
   ```

---

### Method 2: Quick Local Share

If you just want to share with friends quickly:

```powershell
# Run with sharing enabled
streamlit run streamlit_app.py --server.enableXSRF false
```

Then share your **local network URL** (shown in terminal) with people on the same WiFi.

---

## 📋 Deployment Files Needed

### Create `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#764ba2"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
port = 8501
enableCORS = false
```

### Update `requirements.txt`
Make sure it includes:
```
streamlit>=1.28.0
scikit-learn>=1.3.0
numpy>=1.21.0
pillow>=9.0.0
matplotlib>=3.5.0
```

---

## ⚠️ Important Notes

### Model File Issue
The model file (`plant_disease_model_sklearn.pkl`) is **NOT** in GitHub because it's too large (50-200MB).

**Solution for Streamlit Cloud**:

#### Option A: Train on Cloud (Best)
Add `packages.txt`:
```
# No system packages needed
```

Add script to build model during deployment. Streamlit Cloud will automatically run `quick_train.py` if you include the dataset.

#### Option B: Use Cloud Storage
Modify `streamlit_app.py` to download model from Google Drive or AWS S3:

```python
import gdown

MODEL_URL = 'https://drive.google.com/uc?id=YOUR_FILE_ID'

if not os.path.exists('plant_disease_model_sklearn.pkl'):
    st.info("Downloading model...")
    gdown.download(MODEL_URL, 'plant_disease_model_sklearn.pkl', quiet=False)
```

#### Option C: Include Dataset
Since your dataset is already in the repository, Streamlit Cloud can train during deployment:

1. Remove `dataset/` from `.gitignore` (just for one commit)
2. Push the dataset to GitHub
3. Streamlit will run training automatically

---

## 🎯 Quick Commands Reference

```powershell
# Install Streamlit
pip install streamlit

# Run locally
streamlit run streamlit_app.py

# Run with auto-reload on code changes
streamlit run streamlit_app.py --server.runOnSave true

# Stop the server
Ctrl + C

# Check Streamlit version
streamlit --version
```

---

## 🌐 Streamlit vs Flask

| Feature | Streamlit | Flask |
|---------|-----------|-------|
| **Ease of Use** | ✅ Very Easy | ⚠️ Moderate |
| **UI Components** | ✅ Built-in | ❌ Manual HTML/CSS |
| **Deployment** | ✅ Free Cloud | ⚠️ Need Hosting |
| **URL** | `http://localhost:8501` | `http://localhost:5000` |
| **Best For** | Data Science Apps | Production APIs |

---

## 🎨 Customization

### Change Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"  # Red
backgroundColor = "#0E1117"  # Dark
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
```

### Add Logo
```python
st.image("logo.png", width=200)
```

### Add Sidebar Info
```python
with st.sidebar:
    st.header("About")
    st.write("Your custom text here")
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: 
```powershell
pip install streamlit
```

### Issue: "Address already in use"
**Solution**: 
```powershell
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Model not found
**Solution**: 
```powershell
python quick_train.py
```

### Issue: Blank screen on deployment
**Solution**: Check logs on Streamlit Cloud dashboard. Usually means missing model file.

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: https://github.com/AeroLakshyaM/plant-disease-detection/issues

---

🎉 **You're ready to deploy!** Start with local testing, then push to Streamlit Cloud for free hosting!
