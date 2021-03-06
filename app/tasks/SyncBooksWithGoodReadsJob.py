from app.utils.flask_sqlite_queue import Job
from app import app, queue, db
from app.models import Book, Genre

from datetime import datetime, timedelta

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree

class SyncBooksWithGoodReadsJob(Job):
    
    def __init__(self, repeat = True):
        Job.__init__(self)
        self.repeat = repeat
    
    def run(self):
        if self.repeat:
            self._schedule_next_run()
        for book in Book.query.all():
            self._sync_book_with_goodreads(book)

    def _schedule_next_run(self):
        today = datetime.utcnow()
        tomorrow = today + timedelta(days=1)
        tomorrow_1_am = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour = 1, tzinfo = None )

        queue.schedule(self, tomorrow_1_am)

    def _sync_book_with_goodreads(self, book):
        book_id = self._get_id_for_isbn(book.isbn13)

        if book_id is None:
            return

        book_data = self._get_book_data(book_id)

        if book_data is None:
            return

        decoded_book_data = self._parse_XML(book_data)

        # make sure all genres exit in our database bevor adding them to the book
        genres = []
        genre_title_blacklist = ['book', 'read', 'shelf', 'own']
        for genre_title in decoded_book_data['genres']:
            is_blacklisted = False
            for blacklisted_title in genre_title_blacklist:
                is_blacklisted = is_blacklisted or (blacklisted_title in genre_title.lower())
            if not is_blacklisted:
                genre = Genre.query.filter_by(title=genre_title).first()
                if genre is None:
                    genre = Genre(genre_title)
                    db.session.add(genre)
                    db.session.commit()
                genres.append(genre)
        
        book.title = decoded_book_data['title']
        book.author = decoded_book_data['author']
        book.rating = decoded_book_data['rating']
        book.description = decoded_book_data['description']
        if (book.cover_image_url is None) or ('goodreads' in book.cover_image_url):
            book.cover_image_url = decoded_book_data['cover_image_url']
        book.goodreads_url = decoded_book_data['goodreads_url']
        book.goodreads_author_url = decoded_book_data['goodreads_author_url']

        book.genres = genres
        
        db.session.commit()
    
    def _get_id_for_isbn(self, isbn):
        url = self._get_isbn_to_id_endpoint(isbn)
        try:
            response = urlopen(url)
        except HTTPError as e:
            # Return code error (e.g. 404, 501, ...
            print('HTTPError: {}'.format(e.code), '<' + url + '>')
            return None
        except URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URLError: {}'.format(e.reason), '<' + url + '>')
            return None
        else:
            # 200
            return(int(response.read()))

    def _get_book_data(self, id):
        url = self._get_book_data_endpoint(id)
        try:
            response = urlopen(url)
        except HTTPError as e:
            # Return code error (e.g. 404, 501, ...
            print('HTTPError: {}'.format(e.code), '<' + url + '>')
            return None
        except URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URLError: {}'.format(e.reason), '<' + url + '>')
            return None
        else:
            # 200
            return response.read()

    def _get_isbn_to_id_endpoint(self, isbn):
        endpoint = 'https://www.goodreads.com/book/isbn_to_id'
        url_values = urlencode({
            'key': self._get_api_key(),
            'isbn': str(isbn)
        })
        full_url = endpoint + '?' + url_values
        return full_url

    def _get_book_data_endpoint(self, id):
        endpoint = 'https://www.goodreads.com/book/show.xml'
        url_values = urlencode({
            'key': self._get_api_key(),
            'format': 'xml',
            'id': str(id)
        })
        full_url = endpoint + '?' + url_values
        return full_url
        
    def _get_api_key(self):
        return app.config['GOODREADS_API_KEY']

    def _parse_XML(self, raw_xml_response):
        tree = ElementTree.fromstring(raw_xml_response)
        book = tree[1]
        return {
            'title': book.find('title').text,
            'author': book.find('authors')[0].find('name').text,
            'rating': float(book.find('average_rating').text),
            'description': book.find('description').text,
            'cover_image_url': book.find('image_url').text,
            'goodreads_url':  book.find('link').text,
            'goodreads_author_url': book.find('authors')[0].find('link').text,
            'genres': [shelf.attrib['name'] for shelf in book.find('popular_shelves')[:5]]
        }
