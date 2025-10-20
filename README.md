# Bollywood Quiz Application

A comprehensive web-based quiz application featuring popular Bollywood movies from the 1990s onwards. Test your knowledge of Hindi cinema with questions of varying difficulty levels!

## Features

- **50+ Bollywood Movies**: Curated collection from 1990s to present
- **4 Difficulty Levels**: Easy (10 pts), Medium (20 pts), Hard (30 pts), Expert (40 pts)  
- **8 Question Quiz**: 2 questions from each difficulty level
- **Player Scoring**: Track scores and maintain leaderboard
- **Responsive Design**: Beautiful UI with Bootstrap and custom CSS
- **Database Storage**: SQLite database for movies, questions, and player data

## Movie Collection

The quiz includes popular movies such as:
- Dilwale Dulhania Le Jayenge (1995)
- 3 Idiots (2009) 
- Lagaan (2001)
- Dangal (2016)
- Queen (2013)
- Zindagi Na Milegi Dobara (2011)
- And many more classics!

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Data Collection**: Beautiful Soup for web scraping
- **Styling**: Custom CSS with gradients and animations

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd AppWithDB
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   
   **Option A: Using the batch file (Windows)**
   ```bash
   run_quiz.bat
   ```
   
   **Option B: Manual setup**
   ```bash
   # Initialize database
   python setup_database.py
   
   # Run the application
   python app.py
   ```

4. **Access the quiz**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Enter your name and start the quiz!

## Database Schema

### Movies Table
- id (Primary Key)
- title, release_year, director, producer
- music_director, cast, plot, genre

### Questions Table  
- id (Primary Key)
- movie_id (Foreign Key)
- question_text, difficulty_level, points

### Answers Table
- id (Primary Key) 
- question_id (Foreign Key)
- answer_text, is_correct

### Players Table
- id (Primary Key)
- name, final_score, date_played

## Quiz Rules

1. **8 Questions Total**: 2 from each difficulty level
2. **Scoring**: 10, 20, 30, 40 points based on difficulty
3. **Maximum Score**: 200 points (8 × average 25 points)
4. **Question Selection**: Randomized from available pool
5. **No Time Limit**: Take your time to think!

## File Structure

```
AppWithDB/
├── app.py                 # Main Flask application
├── scraper.py            # Movie data collection
├── init_db.py            # Database initialization  
├── setup_database.py     # Database setup script
├── run_quiz.bat          # Windows batch launcher
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Landing page
│   ├── quiz.html        # Quiz interface
│   ├── results.html     # Results page
│   └── leaderboard.html # Leaderboard
└── static/              # Static files (CSS/JS)
```

## Customization

### Adding More Movies
1. Edit `scraper.py` and add movie data to the `bollywood_movies` list
2. Re-run `python setup_database.py` to rebuild the database

### Adding Custom Questions
1. Edit `init_db.py` and add entries to the `questions_data` dictionary
2. Follow the format: question, 4 options, correct answer index, difficulty level

### Styling Changes
1. Modify the CSS in `templates/base.html`
2. Update Bootstrap classes in individual templates

## Troubleshooting

### Common Issues

1. **Python not found**
   - Install Python from https://python.org/downloads/
   - Ensure Python is added to system PATH

2. **Database errors**
   - Delete `bollywood_quiz.db` if it exists
   - Re-run `python setup_database.py`

3. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

4. **Missing dependencies**
   - Run `pip install -r requirements.txt` again
   - Check for Python version compatibility

## Contributing

Feel free to contribute by:
- Adding more movies and questions
- Improving the UI/UX design
- Adding new features (timers, categories, etc.)
- Fixing bugs or improving performance

## License

This project is for educational purposes. Movie data is used for fair use educational content.

## Contact

For questions or suggestions, please open an issue in the repository.

---

Enjoy testing your Bollywood knowledge! 🎬✨
90s bollywood quiz
