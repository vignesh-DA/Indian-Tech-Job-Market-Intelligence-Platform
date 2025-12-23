@echo off
REM Windows Startup Script for Indian Tech Job Intelligence Platform

echo ================================================
echo Indian Tech Job Market Intelligence Platform
echo ================================================
echo.

REM Check if virtual environment exists
if exist venv\ (
    echo [1/3] Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo Warning: Virtual environment not found
    echo Run: python -m venv venv
    echo.
)

REM Check if dependencies are installed
echo [2/3] Checking dependencies...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies OK
)

echo [3/3] Starting Streamlit app...
echo.
echo App will open at: http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

REM Start the app
streamlit run app.py

pause
