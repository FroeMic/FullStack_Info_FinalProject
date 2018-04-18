from .book import Book
from .mood import Mood
from .genre import Genre
from .book_genre import BookGenre
from .book_mood import BookMood
from .search_query_result import SearchQueryResult

from app import db

class SearchQuery(object):

    def __init__(self, moods, limit = 100, min_score = 0.7):
        self.moods = moods
        self.limit = limit
        self.min_score = min_score

    def get_results(self):
        query = self._build_query()
        rows = db.engine.execute(query)
        return [self._make_query_result(row) for row in rows]


    def _build_query(self):
        query = ' '.join([
            'SELECT b.id, b.isbn, b.isbn13, b.title, b.author, b.price, b.rating, b.description, b.cover_image_url, b.goodreads_url, b.goodreads_author_url, b.amazon_url, b.created_at, b.updated_at, AVG(COALESCE(bm.score,0)) AS total_score',
            'FROM {} m, {} b, {} bg, {} g'.format(Mood.__table__, Book.__table__, BookGenre.__table__, Genre.__table__),
            'LEFT JOIN book_mood bm ON m.id = bm.mood_id',
            'WHERE bm.book_id = b.id',
            'AND bg.book_id = b.id',
            'AND bg.genre_id = g.id',
            'AND m.id in ({})'.format(self._get_mood_query_string()),
            'GROUP BY b.id, b.isbn, b.isbn13, b.title, b.author, b.price, b.rating, b.description, b.cover_image_url, b.goodreads_url, b.goodreads_author_url, b.amazon_url, b.created_at, b.updated_at',
            'HAVING total_score > {}'.format(self.min_score),
            'ORDER BY total_score DESC',
            'LIMIT {}'.format(self.limit)
        ])

        return query


    def _get_mood_query_string(self):
        moods = self.moods
        print(','.join(['{}'.format(mood.id) for mood in moods]))
        return ','.join(['{}'.format(mood.id) for mood in moods])


    def _make_query_result(self, row):
        return SearchQueryResult(row['total_score'], Book(row))

