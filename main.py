from app import app
import views
from flask import session

if __name__ == '__main__':
    with app.test_request_context():  # Ensure we are in the app context to clear the session
        session.pop('user_id', None) 
    app.run(debug=True)