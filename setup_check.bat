@echo off
REM Setup verification script for Package Damage Prediction project

echo ========================================
echo Python Installation Check
echo ========================================
echo.

REM Try different Python commands
echo Checking for Python installation...
echo.

REM Method 1: python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found via 'python' command
    python --version
    set PYTHON_CMD=python
    goto :check_pip
)

REM Method 2: python3 command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found via 'python3' command
    python3 --version
    set PYTHON_CMD=python3
    goto :check_pip
)

REM Method 3: py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found via 'py' launcher
    py --version
    set PYTHON_CMD=py
    goto :check_pip
)

REM No Python found
echo [ERROR] Python is NOT properly installed!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation:
echo   1. Check "Add Python to PATH"
echo   2. Choose "Install for all users" (if available)
echo   3. Restart your terminal after installation
echo.
pause
exit /b 1

:check_pip
echo.
echo ========================================
echo Checking pip (package manager)...
echo ========================================
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available
    echo Please reinstall Python and ensure pip is included
    pause
    exit /b 1
)
echo [OK] pip is available
%PYTHON_CMD% -m pip --version
echo.

echo ========================================
echo Checking Required Packages
echo ========================================
echo.

set ALL_INSTALLED=1

echo Checking numpy...
%PYTHON_CMD% -c "import numpy; print(f'  Version: {numpy.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] numpy
    set ALL_INSTALLED=0
) else (
    echo [OK] numpy
)

echo Checking pandas...
%PYTHON_CMD% -c "import pandas; print(f'  Version: {pandas.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] pandas
    set ALL_INSTALLED=0
) else (
    echo [OK] pandas
)

echo Checking scikit-learn...
%PYTHON_CMD% -c "import sklearn; print(f'  Version: {sklearn.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] scikit-learn
    set ALL_INSTALLED=0
) else (
    echo [OK] scikit-learn
)

echo Checking matplotlib...
%PYTHON_CMD% -c "import matplotlib; print(f'  Version: {matplotlib.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] matplotlib
    set ALL_INSTALLED=0
) else (
    echo [OK] matplotlib
)

echo Checking seaborn...
%PYTHON_CMD% -c "import seaborn; print(f'  Version: {seaborn.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] seaborn
    set ALL_INSTALLED=0
) else (
    echo [OK] seaborn
)

echo Checking streamlit...
%PYTHON_CMD% -c "import streamlit; print(f'  Version: {streamlit.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] streamlit
    set ALL_INSTALLED=0
) else (
    echo [OK] streamlit
)

echo Checking plotly...
%PYTHON_CMD% -c "import plotly; print(f'  Version: {plotly.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo [MISSING] plotly
    set ALL_INSTALLED=0
) else (
    echo [OK] plotly
)

echo.
if %ALL_INSTALLED% equ 0 (
    echo ========================================
    echo Installing Missing Packages
    echo ========================================
    echo.
    echo Installing required packages...
    %PYTHON_CMD% -m pip install numpy pandas scikit-learn matplotlib seaborn streamlit plotly
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Package installation failed
        echo Please try manually: %PYTHON_CMD% -m pip install numpy pandas scikit-learn matplotlib seaborn streamlit plotly
        pause
        exit /b 1
    )
    echo.
    echo [OK] All packages installed successfully!
) else (
    echo [OK] All required packages are installed!
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run the pipeline using:
echo   run_pipeline.bat
echo.
pause
