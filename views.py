from flask import Flask, render_template, request, redirect, Blueprint, url_for, flash, session
from models import db, InputData, User, Question, QuestionB, QuestionC, QuestionD, Responses, College, Campus, Prgrms, Fclty
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy import func


analyzer = SentimentIntensityAnalyzer()

views = Blueprint('views', __name__,)

@views.route('/slee')
def slee():
    questions = Question.query.all()
    questionsb = QuestionB.query.all()
    questionsc = QuestionC.query.all()
    questionsd = QuestionD.query.all()
    colleges = College.query.all()
    campus = Campus.query.all()
    program = Prgrms.query.all()
    faculty = Fclty.query.all()
    return render_template('slee.html', questions=questions, questionsb=questionsb, questionsc=questionsc, questionsd=questionsd, colleges=colleges, campus=campus, program=program, faculty=faculty)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.slee'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('views.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('views.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('views.login'))

    return render_template('register.html')

@views.route('/logout')
def logout():
    session.clear() 
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('views.slee')) 

@views.route('/')
def index():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.slee'))
    questions = Question.query.all()
    questionsb = QuestionB.query.all()
    questionsc = QuestionC.query.all()
    questionsd = QuestionD.query.all()
    colleges = College.query.all()
    campus = Campus.query.all()
    program = Prgrms.query.all()
    faculty = Fclty.query.all()
    return render_template('index.html', questions=questions, questionsb=questionsb, questionsc=questionsc, questionsd=questionsd, colleges=colleges, campus=campus, program=program, faculty=faculty)

@views.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('comments')
    email = request.form.get('email')
    idnum = request.form.get('idnumber')
    campus = request.form.get('campus')
    college = request.form.get('college')
    program = request.form.get('program')
    year = request.form.get('year')
    faculty = request.form.get('faculty')

    new_input = InputData(user_input=user_input, email=email, idnum=idnum, campus=campus, college=college, program=program, year=year, faculty=faculty)

    db.session.add(new_input)

    question = Question.query.all()
    for question in question:
        answer = request.form.get(f'question_{question.id}')
        if answer:
            new_response = Responses(email=email, faculty=faculty, qletter="A", qid=question.id, answer=int(answer))
            db.session.add(new_response)

    questionb = QuestionB.query.all()
    for question in questionb:
        answer = request.form.get(f'questionb_{question.id}')
        if answer:
            new_response = Responses(email=email, faculty=faculty, qletter="B", qid=question.id, answer=int(answer))
            db.session.add(new_response)

    questionc = QuestionC.query.all()
    for question in questionc:
        answer = request.form.get(f'questionc_{question.id}')
        if answer:
            new_response = Responses(email=email, faculty=faculty, qletter="C", qid=question.id, answer=int(answer))
            db.session.add(new_response)

    questiond = QuestionD.query.all()
    for question in questiond:
        answer = request.form.get(f'questiond_{question.id}')
        if answer:
            new_response = Responses(email=email, faculty=faculty, qletter="D", qid=question.id, answer=int(answer))
            db.session.add(new_response)

    db.session.commit()

    if 'user_id' not in session:
        return redirect(url_for('views.slee'))
    else:
        return redirect('/')

@views.route('/analyze_sentiment', methods=['GET'])
def analyze_sentiment():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.slee'))
    all_inputs = InputData.query.all()
    all_responses = Responses.query.all()

    total_score = 0
    num_inputs = len(all_inputs)

    for input_data in all_inputs:
        sentiment = analyzer.polarity_scores(input_data.user_input)
        total_score += sentiment['compound']  


    average_score = total_score / num_inputs if num_inputs > 0 else 0 

    total_answers = sum(response.answer for response in all_responses)
    num_responses = len(all_responses)
    average_answer = total_answers / num_responses if num_responses > 0 else 0

  
    return render_template('vaderresult.html', average_score=average_score, average_answer=average_answer, num_inputs=num_inputs)

@views.route('/settings')
def settings():
    return render_template('settingsbase.html')

from sqlalchemy import func

@views.route('/faculty-averages')
def faculty_averages():
    faculty_counts = db.session.query(
        Responses.faculty,
        func.count(Responses.id).label('response_count')  
    ).group_by(Responses.faculty).all()

    averages = db.session.query(
        Responses.faculty,
        Responses.qletter,
        func.avg(Responses.answer).label('average_answer')
    ).filter(
        Responses.qletter.in_(['A', 'B', 'C', 'D'])
    ).group_by(
        Responses.faculty, Responses.qletter
    ).order_by(
        Responses.faculty, Responses.qletter
    ).all()

    faculty_averages = {}

    for faculty, _ in faculty_counts:
        faculty_averages[faculty] = {
            'A': None, 'B': None, 'C': None, 'D': None, 'total': 0 
        }

    for faculty, qletter, avg in averages:
        faculty_averages[faculty][qletter] = round(avg, 2)

    for faculty, response_count in faculty_counts:
        total_instances = response_count // 21 
        faculty_averages[faculty]['total'] = total_instances

    data = []
    for faculty, averages in faculty_averages.items():
        data.append({
            'faculty': faculty,
            'A': averages['A'],
            'B': averages['B'],
            'C': averages['C'],
            'D': averages['D'],
            'total': averages['total'] 
        })

    return render_template('viewresult.html', data=data)

@views.route('/clear_data', methods=['POST'])
def clear_data():
    try:
        db.session.query(Responses).delete()

        db.session.query(InputData).delete()
        
        db.session.commit()
        flash("All data has been cleared successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing data: {e}", "danger")
    
    return redirect(url_for('views.settings'))