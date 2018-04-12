from app import db
from datetime import datetime

class BookGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=False)
    book = db.relationship('Book',
        backref=db.backref('book_genres', lazy=True))

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),
        nullable=False)
    genre = db.relationship('Genre',
        backref=db.backref('book_genres', lazy=True))