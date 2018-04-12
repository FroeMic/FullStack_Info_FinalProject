from app import db
from datetime import datetime

class BookMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=False)
    book = db.relationship('Book',
        backref=db.backref('book_moods', lazy=True))

    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'),
        nullable=False)
    mood = db.relationship('Mood',
        backref=db.backref('book_moods', lazy=True))
