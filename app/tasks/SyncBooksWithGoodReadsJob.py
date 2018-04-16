from app.utils.flask_sqlite_queue import Job
from app import app, queue
from app.models import Book

from urllib.request import urlopen
from urllib.parse import urlencode
from xml.etree import ElementTree

class SyncBooksWithGoodReadsJob(Job):
    
    def __init__(self):
        Job.__init__(self)
    
    def run(self):
        print('START SyncBooksWithGoodReadsJob Job')
        # req = urllib2.Request('http://www.voidspace.org.uk')
        # response = urllib2.urlopen(req)
        # the_page = response.read()
        # queue.delay(self, 5)
        book_id = self._get_id_for_isbn('9780692625477')
        book_data = self._get_book_data(book_id)
        decoded_book_data = self._parse_XML(book_data)
        print(book_id)
    
    def _get_id_for_isbn(self, isbn):
        url = self._get_isbn_to_id_endpoint(isbn)
        try:
            response = urlopen(url)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...
            print('HTTPError: {}'.format(e.code))
            return None
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URLError: {}'.format(e.reason))
            return None
        else:
            # 200
            return(int(response.read()))

    def _get_book_data(self, id):
        url = self._get_book_data_endpoint(id)
        try:
            response = urlopen(url)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...
            print('HTTPError: {}'.format(e.code))
            return None
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URLError: {}'.format(e.reason))
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
        # root = tree.getroot()
        # for child in tree[1]:
        #     print(child.tag, child.attrib)
        book = tree[1]
        print(book.find('title').text)
