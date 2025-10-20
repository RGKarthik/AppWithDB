"""
Direct Python launcher for Bollywood Quiz
Run this file directly to bypass batch file issues
"""
import sys
import subprocess
import os

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        try:
            # Try with --user flag
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', package])
            return True
        except subprocess.CalledProcessError:
            return False

def check_and_install_dependencies():
    """Check and install required packages"""
    required_packages = [
        'flask',
        'flask-sqlalchemy', 
        'requests',
        'beautifulsoup4',
        'lxml',
        'werkzeug',
        'python-dotenv'
    ]
    
    print("🔍 Checking dependencies...")
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def run_quiz():
    """Run the Bollywood Quiz application"""
    print("🎬 Starting Bollywood Quiz Application...")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check dependencies
    if not check_and_install_dependencies():
        print("\n❌ Failed to install dependencies!")
        print("Please try running as administrator or install manually:")
        print("pip install flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv")
        input("\nPress Enter to exit...")
        return
    
    # Import and run the app
    try:
        print("\n🚀 Starting Flask server...")
        print("📱 Open your browser to: http://localhost:5000")
        print("📊 Database status: http://localhost:5000/status")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
        # Import and run the Flask app
        import app
        app.app.run(debug=True, host='127.0.0.1', port=5000)
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("There might be an issue with the app.py file")
    except KeyboardInterrupt:
        print("\n\n👋 Quiz application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    run_quiz()