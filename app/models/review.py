from app import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, index=False)
    text = db.Column(db.Text, index=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('reviews', lazy=True))

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=False)
    book = db.relationship('Book',
        backref=db.backref('reviews', lazy=True))

    moods = db.relationship('Mood', secondary='review_mood', lazy='subquery',
        backref=db.backref('reviews', lazy=True))