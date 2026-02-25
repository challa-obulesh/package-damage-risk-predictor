@echo off
REM Batch script to run the complete package damage prediction pipeline

echo ========================================
echo Logistics Package Damage Prediction
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

REM Step 1: Generate Data
echo [Step 1/3] Generating synthetic shipping dataset...
python src\generate_data.py
if %errorlevel% neq 0 (
    echo ERROR: Data generation failed
    pause
    exit /b 1
)
echo.

REM Step 2: Train Model
echo [Step 2/3] Training classification models...
python src\train_model.py
if %errorlevel% neq 0 (
    echo ERROR: Model training failed
    pause
    exit /b 1
)
echo.

REM Step 3: Analyze Risks
echo [Step 3/3] Analyzing risk factors...
python src\analyze_risks.py
if %errorlevel% neq 0 (
    echo ERROR: Risk analysis failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Pipeline completed successfully!
echo ========================================
echo.
echo Check the 'output' directory for:
echo   - Feature importance charts
echo   - Risk analysis visualizations
echo   - Comprehensive risk report
echo.
pause
