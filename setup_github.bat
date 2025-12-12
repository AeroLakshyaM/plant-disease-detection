@echo off
REM GitHub Setup Helper Script

echo ============================================================
echo GitHub Setup - Plant Disease Detection
echo ============================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1] Git is installed: OK
echo.

REM Check if already initialized
if exist ".git" (
    echo [2] Git repository already exists
    echo.
    goto :update
) else (
    goto :initialize
)

:initialize
echo [2] Initializing Git repository...
git init
echo.

echo [3] Creating .gitignore...
if not exist ".gitignore" (
    echo .gitignore already exists
)
echo.

echo [4] Adding files...
git add .
echo.

echo [5] Creating first commit...
git commit -m "Initial commit: Complete plant disease detection system"
echo.

echo ============================================================
echo Next Steps:
echo ============================================================
echo.
echo 1. Create a repository on GitHub:
echo    - Go to: https://github.com/new
echo    - Name: plant-disease-detection
echo    - Don't initialize with README
echo.
echo 2. Copy your repository URL (it will look like):
echo    https://github.com/YOUR_USERNAME/plant-disease-detection.git
echo.
set /p repo_url="3. Paste your GitHub repository URL here: "
echo.

if "%repo_url%"=="" (
    echo [ERROR] No URL provided!
    pause
    exit /b 1
)

echo [6] Connecting to GitHub...
git remote add origin %repo_url%
echo.

echo [7] Pushing to GitHub...
git branch -M main
git push -u origin main
echo.

if errorlevel 1 (
    echo.
    echo [INFO] If authentication failed:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Generate new token (classic)
    echo 3. Select 'repo' scope
    echo 4. Copy token and use as password when prompted
    echo.
    pause
    exit /b 1
)

echo ============================================================
echo Success! Your project is now on GitHub!
echo ============================================================
echo.
echo View your repository at:
echo %repo_url%
echo.
goto :end

:update
echo ============================================================
echo Updating Existing Repository
echo ============================================================
echo.

echo Checking for changes...
git status
echo.

set /p commit_msg="Enter commit message (or press Enter to skip): "

if "%commit_msg%"=="" (
    echo No changes to commit
    goto :end
)

echo.
echo Adding changes...
git add .
echo.

echo Creating commit...
git commit -m "%commit_msg%"
echo.

echo Pushing to GitHub...
git push
echo.

if errorlevel 1 (
    echo [ERROR] Push failed. Try: git pull origin main --rebase
    pause
    exit /b 1
)

echo ============================================================
echo Successfully updated GitHub repository!
echo ============================================================
echo.

:end
echo Commands you can use:
echo   git status          - Check what changed
echo   git add .           - Stage all changes
echo   git commit -m "msg" - Commit changes
echo   git push            - Push to GitHub
echo   git pull            - Pull from GitHub
echo.
pause
