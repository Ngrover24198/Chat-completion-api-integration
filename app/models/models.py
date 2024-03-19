from datetime import datetime
from app.extensions import db


# creating the database class to log entries directly into db.
class chatApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    prompt = db.Column(db.String, nullable=False)
    completion = db.Column(db.String, nullable=False)
