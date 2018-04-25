from app.utils.flask_sqlite_queue import Job
from app import app, queue, db
from app.models import Book, Genre

from datetime import datetime, timedelta

from amazon.api import AmazonAPI, AsinNotFound
from urllib.error import HTTPError

class SyncBooksWithAmazonJob(Job):
    
    def __init__(self, repeat = True):
        Job.__init__(self)
        self.amazon = None
        self.repeat = repeat
    
    def run(self):
        if self.repeat:
            self._schedule_next_run()

        self.amazon = AmazonAPI(app.config['AMAZON_ACCESS_KEY'], app.config['AMAZON_SECRET_KEY'], app.config['AMAZON_ASSOC_TAG'], region='US')
        for book in Book.query.all():
            try:
                self._sync_book_with_amazon(book)
            except:
                pass

    def _schedule_next_run(self):
        today = datetime.utcnow()
        tomorrow = today + timedelta(days=1)
        tomorrow_2_am = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour = 2, tzinfo = None )

        queue.schedule(self, tomorrow_2_am)

    def _sync_book_with_amazon(self, book):
        try:
            self._sync_book_with_amazon_using_itemid(book, book.isbn13)
        except AsinNotFound:
            try:
                self._sync_book_with_amazon_using_itemid(book, book.isbn)
            except AsinNotFound:
                print('Book ({}) not found on Amazon.'.format(book.isbn13))
            except HTTPError as httperror:
                print('Book ({}) Http Error'.format(book.isbn13), httperror)
        except HTTPError as httperror:
            print('Book ({}) Http Error'.format(book.isbn13), httperror)

    def _sync_book_with_amazon_using_itemid(self, book, itemId):
        products = self.amazon.lookup(SearchIndex='Books', IdType='ISBN', ItemId=itemId)

        if type(products) is list and len(products) > 0:
            book.amazon_url = products[0].offer_url
            book.price = products[0].price_and_currency[0]
            if products[0].large_image_url is not None:
                book.cover_image_url = products[0].large_image_url
        else:
            book.amazon_url = products.offer_url
            book.price = products.price_and_currency[0]
            if products.large_image_url is not None:
                book.cover_image_url = products.large_image_url

        db.session.commit()