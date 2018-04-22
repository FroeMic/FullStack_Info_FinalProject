from app.utils.flask_sqlite_queue import Job
from app import app, queue, db
from app.models import Book, Genre

from datetime import datetime, timedelta

from amazon.api import AmazonAPI, AsinNotFound

class SyncBooksWithAmazonJob(Job):
    
    def __init__(self, repeat = True):
        Job.__init__(self)
        self.repeat = repeat
    
    def run(self):
        if self.repeat:
            self._schedule_next_run()
        for book in Book.query.all():
            self._sync_book_with_amazon(book)

    def _schedule_next_run(self):
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        tomorrow_2_am = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour = 2, tzinfo = None )

        queue.schedule(self, tomorrow_2_am)

    def _sync_book_with_amazon(self, book):
        amazon = AmazonAPI(app.config['AMAZON_ACCESS_KEY'], app.config['AMAZON_SECRET_KEY'], app.config['AMAZON_ASSOC_TAG'])

        try:
            products = amazon.lookup(SearchIndex='Books', IdType='ISBN', ItemId=book.isbn13)

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

        except AsinNotFound:
            pass

        db.session.commit()