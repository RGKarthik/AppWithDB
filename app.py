from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bollywood_quiz_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bollywood_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(200))
    producer = db.Column(db.String(200))
    music_director = db.Column(db.String(200))
    cast = db.Column(db.Text)
    plot = db.Column(db.Text)
    genre = db.Column(db.String(100))
    questions = db.relationship('Question', backref='movie', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    final_score = db.Column(db.Integer, default=0)
    date_played = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)  # 1=10pts, 2=20pts, 3=30pts, 4=40pts
    points = db.Column(db.Integer, nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    try:
        player_name = request.form.get('player_name')
        if not player_name:
            return redirect(url_for('index'))
        
        # Check if database has questions
        total_questions = Question.query.count()
        if total_questions < 8:
            # Initialize database if no questions exist
            from init_db import init_database
            init_database()
        
        session['player_name'] = player_name
        session['score'] = 0
        session['current_question'] = 0
        session['answers_given'] = []
        
        # Get 8 random questions (2 from each difficulty level)
        questions = []
        for level in [1, 2, 3, 4]:
            level_questions = Question.query.filter_by(difficulty_level=level).all()
            if len(level_questions) >= 2:
                selected_questions = random.sample(level_questions, 2)
            else:
                selected_questions = level_questions
            questions.extend(selected_questions)
        
        if len(questions) < 8:
            # If still not enough questions, get any available questions
            all_questions = Question.query.all()
            questions = random.sample(all_questions, min(8, len(all_questions)))
        
        random.shuffle(questions)
        session['quiz_questions'] = [q.id for q in questions]
        
        return redirect(url_for('quiz'))
        
    except Exception as e:
        print(f"Error in start_quiz: {e}")
        return redirect(url_for('index'))

@app.route('/quiz')
def quiz():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    current_q_index = session.get('current_question', 0)
    quiz_questions = session.get('quiz_questions', [])
    
    if current_q_index >= len(quiz_questions):
        return redirect(url_for('results'))
    
    question_id = quiz_questions[current_q_index]
    question = Question.query.get(question_id)
    answers = Answer.query.filter_by(question_id=question_id).all()
    
    return render_template('quiz.html', 
                         question=question, 
                         answers=answers, 
                         question_num=current_q_index + 1,
                         total_questions=len(quiz_questions))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    answer_id = request.form.get('answer_id')
    current_q_index = session.get('current_question', 0)
    quiz_questions = session.get('quiz_questions', [])
    
    if answer_id:
        answer = Answer.query.get(answer_id)
        question = Question.query.get(answer.question_id)
        
        # Store the answer
        session['answers_given'].append({
            'question_id': question.id,
            'question_text': question.question_text,
            'selected_answer': answer.answer_text,
            'correct_answer': Answer.query.filter_by(question_id=question.id, is_correct=True).first().answer_text,
            'is_correct': answer.is_correct,
            'points_earned': question.points if answer.is_correct else 0
        })
        
        if answer.is_correct:
            session['score'] += question.points
    
    session['current_question'] = current_q_index + 1
    
    if session['current_question'] >= len(quiz_questions):
        return redirect(url_for('results'))
    else:
        return redirect(url_for('quiz'))

@app.route('/results')
def results():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    # Save player score to database
    player = Player(name=session['player_name'], final_score=session['score'])
    db.session.add(player)
    db.session.commit()
    
    # Get top 3 players
    top_players = Player.query.order_by(Player.final_score.desc()).limit(3).all()
    
    return render_template('results.html', 
                         score=session['score'],
                         answers=session['answers_given'],
                         top_players=top_players)

@app.route('/leaderboard')
def leaderboard():
    top_players = Player.query.order_by(Player.final_score.desc()).limit(10).all()
    return render_template('leaderboard.html', players=top_players)

@app.route('/init_db')
def initialize_db():
    """Manual database initialization route for debugging"""
    try:
        from init_db import init_database
        init_database()
        return "Database initialized successfully! <a href='/'>Go back to quiz</a>"
    except Exception as e:
        return f"Error initializing database: {e}"

@app.route('/status')
def status():
    """Show database status for debugging"""
    try:
        movie_count = Movie.query.count()
        question_count = Question.query.count()
        answer_count = Answer.query.count()
        player_count = Player.query.count()
        
        return f"""
        <h2>Database Status</h2>
        <p>Movies: {movie_count}</p>
        <p>Questions: {question_count}</p>
        <p>Answers: {answer_count}</p>
        <p>Players: {player_count}</p>
        <br>
        <a href='/'>Back to Quiz</a> | <a href='/init_db'>Initialize Database</a>
        """
    except Exception as e:
        return f"Error checking status: {e}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Check if database has data, if not initialize it
        if Movie.query.count() == 0:
            print("Database is empty, initializing with movie data...")
            try:
                from init_db import init_database
                init_database()
                print("Database initialized successfully!")
            except Exception as e:
                print(f"Error initializing database: {e}")
                print("You can manually initialize by visiting http://localhost:5000/init_db")
        
        print("Starting Bollywood Quiz Application...")
        print("Access the quiz at: http://localhost:5000")
        print("Database status at: http://localhost:5000/status")
        
    app.run(debug=True, host='127.0.0.1', port=5000)