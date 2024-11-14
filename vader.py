from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from models import InputData

vadercounts = Blueprint('vadercounts', __name__,)

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to classify sentiment
def classify_sentiment(score):
    if 0.21 <= score <= 1.0:
        return 'positive'
    elif -0.2 <= score <= 0.2:
        return 'neutral'
    elif -1.0 <= score <= -0.21:
        return 'negative'
    return 'unknown'

# Route for the main page
@vadercounts.route('/vadercount')
def vadercount():
    # Query all data from the input_data table
    data = InputData.query.all()

    # Analyze and classify each user input's sentiment
    faculty_sentiment = {}
    for entry in data:
        sentiment_score = analyzer.polarity_scores(entry.user_input)['compound']
        sentiment_class = classify_sentiment(sentiment_score)
        
        # Initialize faculty entry if not present
        if entry.faculty not in faculty_sentiment:
            faculty_sentiment[entry.faculty] = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        # Increment count based on sentiment classification
        faculty_sentiment[entry.faculty][sentiment_class] += 1

    # Prepare data for rendering in HTML
    results = [
        {
            'faculty': faculty,
            'positive': counts['positive'],
            'neutral': counts['neutral'],
            'negative': counts['negative']
        }
        for faculty, counts in faculty_sentiment.items()
    ]

    # Render the HTML template with the sentiment data
    return render_template('vadercount.html', results=results)