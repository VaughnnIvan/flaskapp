from flask import Flask, render_template, request, redirect, Blueprint, url_for, flash, session
from models import db, Question, QuestionB, QuestionC, QuestionD

questions = Blueprint('questions', __name__,)

@questions.route('/viewradio')
def show_question():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = Question.query.all()
    return render_template('questions.html', questions=questions)

@questions.route('/addquestion', methods=['POST'])
def add_question():
    question_text = request.form.get('question_text')
    new_question = Question(text=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('questions.show_question'))

@questions.route('/deletequestion', methods=['POST'])
def delete_question():
    question_id = request.form.get('selected_question_id')
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('questions.show_question'))

@questions.route('/viewradiob')
def show_questionb():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = QuestionB.query.all()
    return render_template('questionsb.html', questions=questions)

@questions.route('/addquestionb', methods=['POST'])
def add_questionb():
    question_text = request.form.get('question_text')
    new_question = QuestionB(text=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('questions.show_questionb'))

@questions.route('/deletequestionb', methods=['POST'])
def delete_questionb():
    question_id = request.form.get('selected_question_id')
    question = QuestionB.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('questions.show_questionb'))

@questions.route('/viewradioc')
def show_questionc():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = QuestionC.query.all()
    return render_template('questionsc.html', questions=questions)

@questions.route('/addquestionc', methods=['POST'])
def add_questionc():
    question_text = request.form.get('question_text')
    new_question = QuestionC(text=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('questions.show_questionc'))

@questions.route('/deletequestionc', methods=['POST'])
def delete_questionc():
    question_id = request.form.get('selected_question_id')
    question = QuestionC.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('questions.show_questionc'))

@questions.route('/viewradiod')
def show_questiond():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = QuestionD.query.all()
    return render_template('questionsd.html', questions=questions)

@questions.route('/addquestiond', methods=['POST'])
def add_questiond():
    question_text = request.form.get('question_text')
    new_question = QuestionD(text=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('questions.show_questiond'))

@questions.route('/deletequestiond', methods=['POST'])
def delete_questiond():
    question_id = request.form.get('selected_question_id')
    question = QuestionD.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('questions.show_questiond'))