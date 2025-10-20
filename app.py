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
    player_name = request.form.get('player_name')
    if not player_name:
        return redirect(url_for('index'))
    
    session['player_name'] = player_name
    session['score'] = 0
    session['current_question'] = 0
    session['answers_given'] = []
    
    # Get 8 random questions (2 from each difficulty level)
    questions = []
    for level in [1, 2, 3, 4]:
        level_questions = Question.query.filter_by(difficulty_level=level).all()
        selected_questions = random.sample(level_questions, min(2, len(level_questions)))
        questions.extend(selected_questions)
    
    random.shuffle(questions)
    session['quiz_questions'] = [q.id for q in questions]
    
    return redirect(url_for('quiz'))

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)