#!/bin/bash

# ============================================
# Library Desk Agent - Easy Start Script
# ============================================

echo ""
echo "============================================"
echo "  Library Desk Agent - Starting..."
echo "============================================"
echo ""

# Check if database exists
if [ ! -f "app/db/library.db" ]; then
    echo "[1/3] Database not found. Initializing..."
    python init_db.py
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to initialize database!"
        exit 1
    fi
    echo "Database initialized successfully!"
    echo ""
else
    echo "[1/3] Database found. Skipping initialization."
    echo ""
fi

# Check if dependencies are installed
echo "[2/3] Checking dependencies..."
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies!"
        exit 1
    fi
else
    echo "Dependencies OK!"
fi
echo ""

# Start the server
echo "[3/3] Starting Flask server..."
echo ""
echo "============================================"
echo "  Server will start on http://localhost:5000"
echo "  Open app/frontend/index.html in your browser"
echo "  Press Ctrl+C to stop the server"
echo "============================================"
echo ""

cd app/server
python main.py
