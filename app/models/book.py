from app import db
from datetime import datetime
from sqlalchemy.sql.expression import func

class Book(db.Model):
    
    def __init__(self, dict):
        self.id = dict['id']
        self.isbn = dict['isbn']
        self.isbn13 = dict['isbn13']
        self.title = dict['title']
        self.author = dict['author']
        self.price = dict['price']
        self.rating = dict['rating']
        self.description = dict['description']
        self.cover_image_url = dict['cover_image_url']
        self.goodreads_url = dict['goodreads_url']
        self.goodreads_author_url = dict['goodreads_author_url']
        self.amazon_url = dict['amazon_url']
        self.created_at = dict['created_at']
        self.updated_at = dict['updated_at']

    @staticmethod
    def get_random(n=10):
        book_ids = [book.id for book in Book.query.order_by(func.random()).limit(n).all()]
        print(book_ids)
        return Book.query.filter(Book.id.in_(book_ids))

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(128), index=True, nullable=False, unique=True)
    isbn13 = db.Column(db.String(128), index=True, nullable=False, unique=True)
    title = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128), index=False)
    price = db.Column(db.Float, index=False)
    rating = db.Column(db.Float, index=False)
    description = db.Column(db.Text, index=False)
    cover_image_url = db.Column(db.String(256), index=False)
    goodreads_url = db.Column(db.String(256), index=False)
    goodreads_author_url = db.Column(db.String(256), index=False)
    amazon_url = db.Column(db.String(256), index=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    genres = db.relationship('Genre', secondary='book_genre', lazy='subquery',
        backref=db.backref('books', lazy=True))

    moods = db.relationship('Mood', secondary='book_mood', lazy='subquery',
        backref=db.backref('books', lazy=True))
