@echo off
REM Start Plant Disease Detection Web App

echo ========================================
echo Plant Disease Detection Web App
echo ========================================
echo.

REM Check if model exists
if not exist "plant_disease_model_sklearn.pkl" (
    echo [WARNING] Model not found!
    echo.
    echo Training model now... This will take 10-20 minutes.
    echo.
    python train_model_sklearn.py
    echo.
    if errorlevel 1 (
        echo [ERROR] Training failed!
        pause
        exit /b 1
    )
)

echo [OK] Model found!
echo.
echo Starting web server...
echo.
echo ========================================
echo Open your browser to:
echo http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
