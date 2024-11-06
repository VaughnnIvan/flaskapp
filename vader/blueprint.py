from flask import Blueprint
from flask import render_template

vader = Blueprint('vader', __name__, template_folder='templates')

@vader.route('/')
def vaderresult():
    return render_template('vader/vaderresult.html')