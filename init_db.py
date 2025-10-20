import json
from app import app, db, Movie, Question, Answer
from scraper import scrape_bollywood_movies

def create_quiz_questions():
    """
    Generate quiz questions for each movie with 4 difficulty levels:
    Level 1 (10 points) - Easy questions about basic movie info
    Level 2 (20 points) - Medium questions about cast/crew
    Level 3 (30 points) - Hard questions about plot details
    Level 4 (40 points) - Expert questions about specific details
    """
    
    questions_data = {
        "Dilwale Dulhania Le Jayenge": [
            # Level 1 - 10 points
            {
                "question": "Who directed the movie 'Dilwale Dulhania Le Jayenge'?",
                "options": ["Aditya Chopra", "Yash Chopra", "Karan Johar", "Sooraj Barjatya"],
                "correct": 0,
                "difficulty": 1
            },
            # Level 2 - 20 points
            {
                "question": "In which year was 'Dilwale Dulhania Le Jayenge' released?",
                "options": ["1994", "1995", "1996", "1997"],
                "correct": 1,
                "difficulty": 2
            },
            # Level 3 - 30 points
            {
                "question": "Who composed the music for 'Dilwale Dulhania Le Jayenge'?",
                "options": ["A.R. Rahman", "Jatin-Lalit", "Shankar-Ehsaan-Loy", "Pritam"],
                "correct": 1,
                "difficulty": 3
            },
            # Level 4 - 40 points
            {
                "question": "What is the name of Kajol's character in 'Dilwale Dulhania Le Jayenge'?",
                "options": ["Simran", "Pooja", "Nisha", "Anjali"],
                "correct": 0,
                "difficulty": 4
            }
        ],
        "Kuch Kuch Hota Hai": [
            {
                "question": "Who directed 'Kuch Kuch Hota Hai'?",
                "options": ["Aditya Chopra", "Karan Johar", "Yash Chopra", "Sooraj Barjatya"],
                "correct": 1,
                "difficulty": 1
            },
            {
                "question": "Which actress played the role of Tina in the movie?",
                "options": ["Kajol", "Rani Mukerji", "Preity Zinta", "Madhuri Dixit"],
                "correct": 1,
                "difficulty": 2
            },
            {
                "question": "What is the name of Shah Rukh Khan's character?",
                "options": ["Raj", "Rahul", "Rohit", "Ravi"],
                "correct": 1,
                "difficulty": 3
            },
            {
                "question": "Who played the role of young Anjali in the movie?",
                "options": ["Sana Saeed", "Pooja Ruparel", "Hansika Motwani", "Fatima Sana Shaikh"],
                "correct": 0,
                "difficulty": 4
            }
        ],
        "Lagaan": [
            {
                "question": "Who directed the movie 'Lagaan'?",
                "options": ["Aamir Khan", "Ashutosh Gowariker", "Rajkumar Hirani", "Farhan Akhtar"],
                "correct": 1,
                "difficulty": 1
            },
            {
                "question": "In which year was 'Lagaan' released?",
                "options": ["2000", "2001", "2002", "2003"],
                "correct": 1,
                "difficulty": 2
            },
            {
                "question": "What sport is central to the plot of 'Lagaan'?",
                "options": ["Football", "Hockey", "Cricket", "Kabaddi"],
                "correct": 2,
                "difficulty": 3
            },
            {
                "question": "Who composed the music for 'Lagaan'?",
                "options": ["A.R. Rahman", "Shankar-Ehsaan-Loy", "Ilaiyaraaja", "Pritam"],
                "correct": 0,
                "difficulty": 4
            }
        ],
        "3 Idiots": [
            {
                "question": "Who directed '3 Idiots'?",
                "options": ["Rajkumar Hirani", "Aamir Khan", "Vidhu Vinod Chopra", "Abhijat Joshi"],
                "correct": 0,
                "difficulty": 1
            },
            {
                "question": "Which engineering college is featured in the movie?",
                "options": ["IIT Delhi", "Imperial College of Engineering", "IIT Bombay", "NIT"],
                "correct": 1,
                "difficulty": 2
            },
            {
                "question": "What is the real name of Aamir Khan's character Rancho?",
                "options": ["Ranchhoddas Chanchad", "Phunsukh Wangdu", "Ranchoddas Shamaldas Chanchad", "Rancho Chanchad"],
                "correct": 2,
                "difficulty": 3
            },
            {
                "question": "What does 'All is Well' signify in the movie?",
                "options": ["A mantra to reduce fear", "A college motto", "A greeting", "A password"],
                "correct": 0,
                "difficulty": 4
            }
        ],
        "Dangal": [
            {
                "question": "Who played the role of Mahavir Singh Phogat in 'Dangal'?",
                "options": ["Aamir Khan", "Akshay Kumar", "Ajay Devgn", "Hrithik Roshan"],
                "correct": 0,
                "difficulty": 1
            },
            {
                "question": "What sport is featured in 'Dangal'?",
                "options": ["Boxing", "Wrestling", "Weightlifting", "Gymnastics"],
                "correct": 1,
                "difficulty": 2
            },
            {
                "question": "Who directed 'Dangal'?",
                "options": ["Rajkumar Hirani", "Nitesh Tiwari", "Aamir Khan", "Ashutosh Gowariker"],
                "correct": 1,
                "difficulty": 3
            },
            {
                "question": "Which Commonwealth Games did Geeta Phogat win gold in?",
                "options": ["2010 Delhi", "2014 Glasgow", "2018 Gold Coast", "2006 Melbourne"],
                "correct": 0,
                "difficulty": 4
            }
        ]
    }
    
    # Generate questions for remaining movies using templates
    question_templates = {
        1: [  # Easy - 10 points
            "Who directed the movie '{title}'?",
            "In which year was '{title}' released?",
            "Who is the lead actor in '{title}'?",
            "What is the genre of '{title}'?"
        ],
        2: [  # Medium - 20 points
            "Who composed the music for '{title}'?",
            "Who produced '{title}'?",
            "Which actress played the female lead in '{title}'?",
            "What is the main theme of '{title}'?"
        ],
        3: [  # Hard - 30 points
            "Who wrote the screenplay for '{title}'?",
            "What awards did '{title}' win?",
            "In which locations was '{title}' primarily shot?",
            "What was the budget of '{title}'?"
        ],
        4: [  # Expert - 40 points
            "What was the box office collection of '{title}'?",
            "Which film festival premiered '{title}'?",
            "What was the working title of '{title}'?",
            "Who was the cinematographer for '{title}'?"
        ]
    }
    
    return questions_data, question_templates

def init_database():
    """Initialize the database with tables and data."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing data
        Answer.query.delete()
        Question.query.delete()
        Movie.query.delete()
        db.session.commit()
        
        # Get movie data from scraper
        movies_data = scrape_bollywood_movies()
        questions_data, question_templates = create_quiz_questions()
        
        print(f"Adding {len(movies_data)} movies to database...")
        
        # Add movies to database
        for movie_data in movies_data:
            movie = Movie(
                title=movie_data['title'],
                release_year=movie_data['release_year'],
                director=movie_data['director'],
                producer=movie_data['producer'],
                music_director=movie_data['music_director'],
                cast=movie_data['cast'],
                plot=movie_data['plot'],
                genre=movie_data['genre']
            )
            db.session.add(movie)
            db.session.flush()  # Get the movie ID
            
            # Add questions for this movie
            if movie_data['title'] in questions_data:
                # Use predefined questions
                movie_questions = questions_data[movie_data['title']]
                for q_data in movie_questions:
                    question = Question(
                        movie_id=movie.id,
                        question_text=q_data['question'],
                        difficulty_level=q_data['difficulty'],
                        points=q_data['difficulty'] * 10
                    )
                    db.session.add(question)
                    db.session.flush()
                    
                    # Add answers
                    for i, option in enumerate(q_data['options']):
                        answer = Answer(
                            question_id=question.id,
                            answer_text=option,
                            is_correct=(i == q_data['correct'])
                        )
                        db.session.add(answer)
            else:
                # Generate generic questions for movies without predefined questions
                for difficulty in range(1, 5):
                    points = difficulty * 10
                    
                    # Generate question based on movie data
                    if difficulty == 1:
                        question_text = f"Who directed the movie '{movie_data['title']}'?"
                        options = [movie_data['director'], "Random Director 1", "Random Director 2", "Random Director 3"]
                        correct_idx = 0
                    elif difficulty == 2:
                        question_text = f"In which year was '{movie_data['title']}' released?"
                        year = movie_data['release_year']
                        options = [str(year), str(year-1), str(year+1), str(year+2)]
                        correct_idx = 0
                    elif difficulty == 3:
                        question_text = f"Who composed the music for '{movie_data['title']}'?"
                        options = [movie_data['music_director'], "A.R. Rahman", "Pritam", "Ilaiyaraaja"]
                        correct_idx = 0
                    else:  # difficulty == 4
                        question_text = f"What is the genre of '{movie_data['title']}'?"
                        options = [movie_data['genre'], "Action", "Thriller", "Horror"]
                        correct_idx = 0
                    
                    question = Question(
                        movie_id=movie.id,
                        question_text=question_text,
                        difficulty_level=difficulty,
                        points=points
                    )
                    db.session.add(question)
                    db.session.flush()
                    
                    # Add answers
                    for i, option in enumerate(options):
                        answer = Answer(
                            question_id=question.id,
                            answer_text=option,
                            is_correct=(i == correct_idx)
                        )
                        db.session.add(answer)
        
        db.session.commit()
        
        # Print statistics
        movie_count = Movie.query.count()
        question_count = Question.query.count()
        answer_count = Answer.query.count()
        
        print(f"Database initialized successfully!")
        print(f"Movies: {movie_count}")
        print(f"Questions: {question_count}")
        print(f"Answers: {answer_count}")
        print(f"Questions per movie: {question_count // movie_count if movie_count > 0 else 0}")

if __name__ == "__main__":
    init_database()