from flask import Flask, render_template, request, redirect, session
from models import db
from vader.blueprint import vader
from views import views
from questions import questions
from fclty import fclty
from pgrm import prgrms
from college import college
from campus import campus
from models import InputData
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = '0514'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///input_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(vader, url_prefix='/vader')
app.register_blueprint(views)
app.register_blueprint(questions)
app.register_blueprint(fclty)
app.register_blueprint(prgrms)
app.register_blueprint(college)
app.register_blueprint(campus)

