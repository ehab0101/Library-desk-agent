@echo off
REM ============================================
REM Library Desk Agent - Easy Start Script
REM ============================================

echo.
echo ============================================
echo   Library Desk Agent - Starting...
echo ============================================
echo.

REM Check if database exists
if not exist "app\db\library.db" (
    echo [1/3] Database not found. Initializing...
    python init_db.py
    if errorlevel 1 (
        echo ERROR: Failed to initialize database!
        pause
        exit /b 1
    )
    echo Database initialized successfully!
    echo.
) else (
    echo [1/3] Database found. Skipping initialization.
    echo.
)

REM Check if dependencies are installed
echo [2/3] Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
) else (
    echo Dependencies OK!
)
echo.

REM Start the server
echo [3/3] Starting Flask server...
echo.
echo ============================================
echo   Server will start on http://localhost:5000
echo   Open app\frontend\index.html in your browser
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

cd app\server
python main.py

pause
