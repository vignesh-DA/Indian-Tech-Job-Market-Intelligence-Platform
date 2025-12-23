#!/bin/bash
# Linux/Mac Startup Script for Indian Tech Job Intelligence Platform

echo "================================================"
echo "Indian Tech Job Market Intelligence Platform"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "[1/3] Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found"
    echo "Run: python3 -m venv venv"
    echo ""
fi

# Check if dependencies are installed
echo "[2/3] Checking dependencies..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Dependencies OK"
fi

echo "[3/3] Starting Streamlit app..."
echo ""
echo "App will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

# Start the app
streamlit run app.py
