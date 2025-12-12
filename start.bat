@echo off
REM Quick Start Script for Plant Disease Detection

echo ============================================================
echo Plant Disease Detection System - Quick Start
echo ============================================================
echo.

REM Check if dataset exists
if not exist "dataset\train" (
    echo [ERROR] Dataset not found!
    echo.
    echo Please run first: python venv\Split_dataset.py
    echo.
    pause
    exit /b 1
)

echo [1] Dataset found: OK
echo.

REM Check Python version
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

echo [2] Python found: OK
echo.

REM Menu
echo ============================================================
echo Choose an option:
echo ============================================================
echo.
echo 1. Train model with TensorFlow (Best accuracy, needs Python 3.11)
echo 2. Train model with Scikit-learn (Works now, good accuracy)
echo 3. Test prediction (TensorFlow model)
echo 4. Test prediction (Scikit-learn model)
echo 5. Verify system setup
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starting TensorFlow training...
    python train_model.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting Scikit-learn training...
    python train_model_sklearn.py
    pause
) else if "%choice%"=="3" (
    echo.
    set /p imgpath="Enter image path: "
    python predict.py "%imgpath%"
    pause
) else if "%choice%"=="4" (
    echo.
    set /p imgpath="Enter image path: "
    python predict_sklearn.py "%imgpath%"
    pause
) else if "%choice%"=="5" (
    echo.
    python quick_test.py
    pause
) else if "%choice%"=="6" (
    exit /b 0
) else (
    echo.
    echo Invalid choice!
    pause
)
