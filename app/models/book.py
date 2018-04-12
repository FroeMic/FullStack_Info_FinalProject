from app import db
from datetime import datetime
from app.models import User

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(128), index=True, nullable=False, unique=True)
    isbn13 = db.Column(db.String(128), index=True, nullable=False, unique=True)
    title = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128), index=False)
    price = db.Column(db.Float, index=False)
    rating = db.Column(db.Float, index=False)
    cover_image_url = db.Column(db.String(256), index=False)
    goodreads_url = db.Column(db.String(256), index=False)
    goodreads_author_url = db.Column(db.String(256), index=False)
    amazon_url = db.Column(db.String(256), index=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)