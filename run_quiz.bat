@echo off
echo Starting Bollywood Quiz Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not found in PATH. Please install Python or add it to PATH.
    echo You can download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Initializing database...
python setup_database.py

if %errorlevel% neq 0 (
    echo Database initialization failed!
    pause
    exit /b 1
)

echo.
echo Database initialized successfully!
echo Starting Flask application...
echo.
echo The quiz will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py