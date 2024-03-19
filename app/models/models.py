from datetime import datetime
from app.extensions import db


# creating the database class to log entries directly into db.
class chatApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    prompt = db.Column(db.String, nullable=False)
    completion = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)


# session class to maintain a userid session throughout the chat
class chatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False, unique=True)
    conversation_history = db.Column(db.Text, nullable=False)
