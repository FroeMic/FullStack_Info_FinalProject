from app import db
from datetime import datetime
from app.models import User, Book

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('bookmarks', lazy=True))

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=False)
    book = db.relationship('Book',
        backref=db.backref('bookmarks', lazy=True))
