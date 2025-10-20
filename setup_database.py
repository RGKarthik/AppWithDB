import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from init_db import init_database
    print("Initializing Bollywood Quiz Database...")
    init_database()
    print("Database initialization completed successfully!")
except Exception as e:
    print(f"Error initializing database: {e}")
    import traceback
    traceback.print_exc()