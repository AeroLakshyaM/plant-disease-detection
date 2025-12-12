@echo off
echo ====================================
echo Pushing to GitHub...
echo ====================================

cd /d "C:\Users\Lakshya mishra\plant_project"

"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Rename streamlit_app.py to app.py for Streamlit Cloud deployment"
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ====================================
echo Done! Now go to Streamlit Cloud and
echo click "Reboot app" button
echo ====================================
pause
