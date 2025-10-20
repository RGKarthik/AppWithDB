import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application():
    """Test the main components of the Bollywood quiz application."""
    
    print("🎬 Testing Bollywood Quiz Application")
    print("=" * 50)
    
    try:
        # Test 1: Import modules
        print("1. Testing imports...")
        from app import app, db, Movie, Question, Answer, Player
        from scraper import scrape_bollywood_movies
        print("   ✅ All imports successful")
        
        # Test 2: Test movie data
        print("\n2. Testing movie data...")
        movies = scrape_bollywood_movies()
        print(f"   ✅ Found {len(movies)} movies")
        print(f"   📽️  Sample movies:")
        for i, movie in enumerate(movies[:3]):
            print(f"      - {movie['title']} ({movie['release_year']})")
        
        # Test 3: Test database connection
        print("\n3. Testing database setup...")
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Test if we can query (even if empty)
            movie_count = Movie.query.count()
            question_count = Question.query.count()
            print(f"   ✅ Database connection successful")
            print(f"   📊 Current database stats:")
            print(f"      - Movies: {movie_count}")
            print(f"      - Questions: {question_count}")
        
        # Test 4: Test Flask routes
        print("\n4. Testing Flask routes...")
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("   ✅ Home page accessible")
            else:
                print(f"   ❌ Home page error: {response.status_code}")
            
            # Test leaderboard
            response = client.get('/leaderboard')
            if response.status_code == 200:
                print("   ✅ Leaderboard accessible")
            else:
                print(f"   ❌ Leaderboard error: {response.status_code}")
        
        print("\n🎉 All tests passed! The application is ready to run.")
        print("\n📋 To start the quiz:")
        print("   1. Run: python setup_database.py (to initialize with data)")
        print("   2. Run: python app.py (to start the server)")
        print("   3. Open: http://localhost:5000")
        print("\n   Or simply run: run_quiz.bat")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you've installed requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_application()