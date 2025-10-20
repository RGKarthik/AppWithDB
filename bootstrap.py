#!/usr/bin/env python3
"""
Bootstrap script for Bollywood Quiz
This script tries to work around Python PATH issues
"""
import sys
import os
import subprocess

def find_python():
    """Find a working Python executable"""
    python_commands = [
        'python',
        'py', 
        'python3',
        os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Microsoft', 'WindowsApps', 'python.exe'),
        r'C:\Python39\python.exe',
        r'C:\Python310\python.exe', 
        r'C:\Python311\python.exe',
        r'C:\Python312\python.exe',
    ]
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Found Python: {cmd}")
                print(f"Version: {result.stdout.strip()}")
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    return None

def install_dependencies(python_cmd):
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        result = subprocess.run([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_app(python_cmd):
    """Run the Flask application"""
    print("🚀 Starting Bollywood Quiz Application...")
    print("📱 Access at: http://localhost:5000")
    print("📊 Database status: http://localhost:5000/status")
    print("💾 Manual DB init: http://localhost:5000/init_db")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([python_cmd, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Quiz application stopped.")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    print("🎬 Bollywood Quiz - Python Bootstrap")
    print("=" * 50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📂 Working directory: {script_dir}")
    
    # Find Python
    python_cmd = find_python()
    if not python_cmd:
        print("\n❌ No Python installation found!")
        print("\n💡 Solutions:")
        print("1. Install Python from https://python.org/downloads")
        print("2. Make sure 'Add Python to PATH' is checked during installation")
        print("3. Or use Microsoft Store Python and enable execution aliases")
        input("\nPress Enter to exit...")
        return 1
    
    # Check/install dependencies
    try:
        subprocess.run([python_cmd, '-c', 'import flask'], 
                      capture_output=True, check=True)
        print("✅ Dependencies already installed")
    except subprocess.CalledProcessError:
        if not install_dependencies(python_cmd):
            input("\nPress Enter to exit...")
            return 1
    
    # Run the application
    run_app(python_cmd)
    return 0

if __name__ == '__main__':
    sys.exit(main())