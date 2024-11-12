from flask import Flask, render_template, request, redirect, Blueprint, url_for, flash, session
from models import db, College

college = Blueprint('college', __name__,)

@college.route('/viewcollege')
def show_college():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('views.login'))
    questions = College.query.all()
    return render_template('college.html', questions=questions)

@college.route('/addcollege', methods=['POST'])
def add_college():
    question_text = request.form.get('question_text')
    new_question = College(college=question_text)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('college.show_college'))

@college.route('/deletecollege', methods=['POST'])
def delete_college():
    question_id = request.form.get('selected_question_id')
    question = College.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('college.show_college'))

