@echo off
echo ================================================================
echo              BOLLYWOOD QUIZ - SIMPLE LAUNCHER
echo ================================================================
echo.

REM Simple approach - try to install Python from Microsoft Store
echo Checking for Python...

REM First, try to enable Microsoft Store Python
echo Trying to install/enable Python from Microsoft Store...
start ms-windows-store://pdp/?productid=9NRWMJP3717K

echo.
echo Please wait for Python installation to complete, then:
echo 1. Close the Microsoft Store window when installation is done
echo 2. Press any key to continue with the quiz setup
echo.
pause

echo Testing Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python still not working. Let's try a different approach...
    echo.
    echo MANUAL SETUP REQUIRED:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.11 or newer
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. After installation, restart this script
    echo.
    pause
    exit /b 1
)

echo Python is now available! Installing packages...
python -m pip install --user flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv

echo.
echo Starting Bollywood Quiz...
echo Open your browser to: http://localhost:5000
echo.
python app.py

pause