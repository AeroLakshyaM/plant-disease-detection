# Deployment Guide - Plant Disease Detection Web App

## 🚀 Quick Start

### 1. Train the Model (First Time Only)

```powershell
python train_model_sklearn.py
```

This will take 10-20 minutes and create:
- `plant_disease_model_sklearn.pkl` (the trained model)
- `class_names.json` (disease class names)

### 2. Run the Web Application

```powershell
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📦 Deployment Options

### Option 1: Local Deployment (Already Done!)

Just run `python app.py` and access locally at `localhost:5000`

### Option 2: Deploy to Render (Free Hosting)

1. **Create account** at https://render.com

2. **Create `Procfile`** (already created):
   ```
   web: gunicorn app:app
   ```

3. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

4. **Connect to Render:**
   - New Web Service
   - Connect your GitHub repo
   - Build Command: `pip install -r requirements.txt && python train_model_sklearn.py`
   - Start Command: `gunicorn app:app`
   - Environment: Python 3

5. **Deploy!** Render will give you a URL like: `your-app.onrender.com`

### Option 3: Deploy to PythonAnywhere (Free)

1. **Create account** at https://www.pythonanywhere.com

2. **Upload your files** via Files tab

3. **Install requirements:**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Train model:**
   ```bash
   python train_model_sklearn.py
   ```

5. **Configure Web App:**
   - Web tab → Add new web app
   - Flask
   - Python version: 3.10 or 3.11
   - Path to Flask app: `/home/yourusername/plant_project/app.py`
   - App name: `app`

6. **Reload web app** - Your site will be at: `yourusername.pythonanywhere.com`

### Option 4: Deploy to Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create app:**
   ```bash
   heroku create your-plant-detector
   ```

3. **Add buildpack:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Scale web dyno:**
   ```bash
   heroku ps:scale web=1
   ```

### Option 5: Deploy to Railway (Recommended - Easy!)

1. **Create account** at https://railway.app

2. **Click "New Project"** → "Deploy from GitHub repo"

3. **Connect your repository**

4. **Railway auto-detects** Flask app and deploys!

5. **Add domain** in Settings

No Procfile or config needed - Railway handles it automatically!

---

## 🔧 Configuration for Production

### Update app.py for Production

Change the last line in [app.py](app.py) from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### Security Improvements

1. **Add secret key** (for sessions):
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
   ```

2. **Add rate limiting** (optional):
   ```bash
   pip install flask-limiter
   ```

3. **Enable CORS** (if needed for API):
   ```bash
   pip install flask-cors
   ```

---

## 📁 Required Files for Deployment

Make sure these files exist:

- ✅ `app.py` - Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - For Heroku/Render
- ✅ `templates/index.html` - Frontend
- ✅ `static/style.css` - Styling
- ✅ `plant_disease_model_sklearn.pkl` - Trained model
- ✅ `class_names.json` - Class labels

---

## 🧪 Testing Before Deployment

1. **Test locally:**
   ```powershell
   python app.py
   ```

2. **Test upload:**
   - Navigate to http://localhost:5000
   - Upload a test image from `dataset/val/`
   - Verify prediction works

3. **Test health endpoint:**
   ```powershell
   curl http://localhost:5000/health
   ```

---

## 🌐 Making It Public

### Share Your Local Server (Temporary)

Use **ngrok** to create a public URL:

1. **Download ngrok:** https://ngrok.com/download

2. **Run your app:**
   ```powershell
   python app.py
   ```

3. **In another terminal:**
   ```powershell
   ngrok http 5000
   ```

4. **Share the ngrok URL** (e.g., `https://abc123.ngrok.io`)

---

## 📊 Performance Tips

### For Faster Predictions:

1. **Reduce MAX_SAMPLES_PER_CLASS** in `train_model_sklearn.py` (smaller model)

2. **Use smaller IMG_SIZE** (64 or 96 instead of 128)

3. **Use fewer estimators** in RandomForest (50 instead of 100)

### For Better Accuracy:

1. **Use Python 3.11** and TensorFlow model

2. **Increase training samples**

3. **Add more data augmentation**

---

## 🆘 Troubleshooting

### Model not found error:
```bash
python train_model_sklearn.py
```

### Port already in use:
```powershell
python app.py --port 5001
```

Or kill the process:
```powershell
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Out of memory during training:
- Reduce `MAX_SAMPLES_PER_CLASS` to 200
- Reduce `IMG_SIZE` to 64

### Slow predictions:
- Reduce `n_estimators` in RandomForest to 50
- Use smaller image size

---

## 🎉 Your App is Ready!

Choose your deployment method and share your plant disease detector with the world!

**Recommended for beginners:** Railway (easiest) or Render (good free tier)

**Best for production:** Heroku or your own VPS
