from flask import Flask, render_template, request, redirect, Blueprint, url_for, flash, session
from models import db, Campus

campus = Blueprint('campus', __name__,)

@campus.route('/viewcampus')
def show_campus():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = Campus.query.all()
    return render_template('campus.html', questions=questions)

@campus.route('/addcampus', methods=['POST'])
def add_campus():
    question_text = request.form.get('question_text')
    new_question = Campus(campus=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('campus.show_campus'))

@campus.route('/deletecampus', methods=['POST'])
def delete_campus():
    question_id = request.form.get('selected_question_id')
    question = Campus.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('campus.show_campus'))

