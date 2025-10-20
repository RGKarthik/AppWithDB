@echo off
echo ================================================================
echo                    BOLLYWOOD QUIZ APPLICATION
echo ================================================================
echo.

REM Try different Python executables
set PYTHON_CMD=

REM Try standard python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo [INFO] Using system Python
    goto :python_found
)

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo [INFO] Using Python Launcher (py)
    goto :python_found
)

REM Try python3 command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo [INFO] Using python3
    goto :python_found
)

REM Try Microsoft Store Python path
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD="C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe"
        echo [INFO] Using Microsoft Store Python
        goto :python_found
    )
)

REM Python not found
echo [ERROR] Python is not found or not properly configured!
echo.
echo SOLUTIONS:
echo 1. Install Python from: https://www.python.org/downloads/
echo    - Make sure to check "Add Python to PATH" during installation
echo.
echo 2. OR fix Microsoft Store Python:
echo    - Go to Settings ^> Apps ^> Advanced app settings ^> App execution aliases
echo    - Enable "App Installer" python.exe and python3.exe
echo.
echo 3. OR install Python manually and add to PATH:
echo    - Download from python.org
echo    - During installation, check "Add Python to PATH"
echo.
pause
exit /b 1

:python_found

echo [INFO] Python found. Checking dependencies...

REM Check if required packages are installed
echo [INFO] Testing Flask import...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Flask not found. Installing required packages...
    echo [DEBUG] Running: %PYTHON_CMD% -m pip install -r requirements.txt
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        echo [DEBUG] Python command used: %PYTHON_CMD%
        echo [INFO] Trying alternative installation method...
        %PYTHON_CMD% -m ensurepip --default-pip >nul 2>&1
        %PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
        %PYTHON_CMD% -m pip install flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv
        if %errorlevel% neq 0 (
            echo [ERROR] Alternative installation also failed!
            echo.
            echo Try manual installation:
            echo 1. Open Command Prompt as Administrator
            echo 2. Run: %PYTHON_CMD% -m pip install flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv
            echo.
            pause
            exit /b 1
        )
    )
) else (
    echo [INFO] Flask already installed
)echo [INFO] Dependencies OK. Starting application...
echo.
echo ================================================================
echo  QUIZ ACCESS INFO:
echo  - Open your browser to: http://localhost:5000
echo  - Database status: http://localhost:5000/status  
echo  - Manual DB init: http://localhost:5000/init_db
echo.
echo  Press Ctrl+C to stop the server
echo ================================================================
echo.

%PYTHON_CMD% app.py

echo.
echo Quiz application has stopped.
pause