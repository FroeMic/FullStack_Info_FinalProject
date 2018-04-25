from app import db
from datetime import datetime

class ReviewMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    review_id = db.Column(db.Integer, db.ForeignKey('review.id'),
        nullable=False)
    review = db.relationship('Review',
        backref=db.backref('review_moods', lazy=True))

    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'),
        nullable=False)
    mood = db.relationship('Mood',
        backref=db.backref('review_moods', lazy=True))
