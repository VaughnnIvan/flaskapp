from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

class QuestionB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

class QuestionC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

class QuestionD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

class InputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    idnum = db.Column(db.String(200), nullable=True)
    campus = db.Column(db.String(200), nullable=False)
    college = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(200), nullable=False)
    faculty = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<InputData {self.user_input}>"
    
class Responses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), db.ForeignKey('input_data.email'), nullable=False)
    faculty = db.Column(db.String(200), db.ForeignKey('input_data.faculty'), nullable=False)
    qletter = db.Column(db.String(200), nullable=False)
    qid = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.Integer, nullable=False)
    
class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(100), nullable=False)
    
class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college = db.Column(db.String(100), nullable=False)

class Prgrms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100), nullable=False)

class Fclty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(100), nullable=False)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)