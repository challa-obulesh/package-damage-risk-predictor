@echo off
REM Launch Streamlit web interface for Package Damage Prediction

echo ========================================
echo Package Damage Risk Predictor
echo ========================================
echo.

REM Try different Python commands
echo Checking for Python installation...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :run_app
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :run_app
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :run_app
)

echo ERROR: Python is not installed or not in PATH
pause
exit /b 1

:run_app
echo Starting Streamlit web interface...
echo.
echo The application will open in your default browser.
echo Press Ctrl+C to stop the server.
echo.

REM Run Streamlit
%PYTHON_CMD% -m streamlit run app.py

pause
