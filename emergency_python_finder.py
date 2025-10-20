"""
Emergency launcher for Bollywood Quiz - No Python PATH required
This file tries to find and use Python even if PATH is broken
"""

import sys
import os
import subprocess
import tempfile

def find_python_executable():
    """Find any working Python executable on the system"""
    
    # Common Python installation paths on Windows
    possible_paths = [
        # Standard installations
        r'C:\Python39\python.exe',
        r'C:\Python310\python.exe', 
        r'C:\Python311\python.exe',
        r'C:\Python312\python.exe',
        r'C:\Program Files\Python39\python.exe',
        r'C:\Program Files\Python310\python.exe',
        r'C:\Program Files\Python311\python.exe',
        r'C:\Program Files\Python312\python.exe',
        r'C:\Program Files (x86)\Python39\python.exe',
        r'C:\Program Files (x86)\Python310\python.exe',
        r'C:\Program Files (x86)\Python311\python.exe',
        r'C:\Program Files (x86)\Python312\python.exe',
        # User installations
        os.path.expanduser(r'~\AppData\Local\Programs\Python\Python39\python.exe'),
        os.path.expanduser(r'~\AppData\Local\Programs\Python\Python310\python.exe'),
        os.path.expanduser(r'~\AppData\Local\Programs\Python\Python311\python.exe'),
        os.path.expanduser(r'~\AppData\Local\Programs\Python\Python312\python.exe'),
        # Anaconda/Miniconda
        r'C:\Anaconda3\python.exe',
        r'C:\Miniconda3\python.exe',
        os.path.expanduser(r'~\Anaconda3\python.exe'),
        os.path.expanduser(r'~\Miniconda3\python.exe'),
    ]
    
    print("🔍 Searching for Python installations...")
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                # Test if this Python works
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Found working Python: {path}")
                    print(f"   Version: {result.stdout.strip()}")
                    return path
            except Exception:
                continue
    
    return None

def create_launcher_script(python_path):
    """Create a launcher script that uses the found Python"""
    
    launcher_content = f'''@echo off
echo ================================================================
echo              BOLLYWOOD QUIZ - EMERGENCY LAUNCHER
echo ================================================================
echo Using Python: {python_path}
echo.

REM Install dependencies
echo Installing dependencies...
"{python_path}" -m pip install --user flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv

echo.
echo Starting Bollywood Quiz...
echo Open browser to: http://localhost:5000
echo.

"{python_path}" app.py

pause
'''
    
    with open('emergency_launcher.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created emergency_launcher.bat")
    return 'emergency_launcher.bat'

def run_directly():
    """Try to run the app directly with found Python"""
    python_path = find_python_executable()
    
    if not python_path:
        print("❌ No Python installation found!")
        print("\n💡 Please install Python from: https://python.org/downloads")
        print("   Make sure to check 'Add Python to PATH' during installation")
        input("\nPress Enter to exit...")
        return False
    
    print(f"\n🚀 Using Python: {python_path}")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    packages = ['flask', 'flask-sqlalchemy', 'requests', 'beautifulsoup4', 'lxml', 'werkzeug', 'python-dotenv']
    
    for package in packages:
        try:
            subprocess.run([python_path, '-c', f'import {package.replace("-", "_")}'], 
                          check=True, capture_output=True)
            print(f"✅ {package} - already installed")
        except subprocess.CalledProcessError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.run([python_path, '-m', 'pip', 'install', '--user', package], 
                              check=True, capture_output=True)
                print(f"✅ {package} - installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}")
    
    # Create emergency launcher for future use
    launcher_file = create_launcher_script(python_path)
    
    # Run the app
    print("\n🎬 Starting Bollywood Quiz...")
    print("📱 Open browser to: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([python_path, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Quiz stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return True

if __name__ == '__main__':
    print("🎬 Bollywood Quiz - Emergency Python Finder")
    print("=" * 50)
    
    # Change to script directory  
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not run_directly():
        # If we can't find Python, show instructions
        print("\n" + "="*50)
        print("PYTHON INSTALLATION REQUIRED")
        print("="*50)
        print("1. Go to: https://python.org/downloads")
        print("2. Download Python 3.11 or newer") 
        print("3. During installation:")
        print("   ✅ Check 'Add Python to PATH'")
        print("   ✅ Check 'Install for all users'")
        print("4. Restart your computer")
        print("5. Run this script again")
        
    input("\nPress Enter to exit...")