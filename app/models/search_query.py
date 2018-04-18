from .book import Book
from .mood import Mood
from .genre import Genre
from .book_genre import BookGenre
from .book_mood import BookMood
from .search_query_result import SearchQueryResult

from app import db

class SearchQuery(object):

    def __init__(self, moods, genres = [], order_by = 'score', limit = 100, min_score = 0.4):
        self.moods = moods
        self.genres = genres
        self.order_by = order_by
        self.limit = limit
        self.min_score = min_score

    def get_results(self):
        query = self._build_query()
        rows = db.engine.execute(query)
        results = [self._make_query_result(row) for row in rows]
        results = self._filter_results(results)
        return results

    def _filter_results(self,results):
        if (len(self.genres) > 0):
            results = self._filter_genres(results)
        
        return results

    def _filter_genres(self, results):
        print('filter genres')
        allowed_genre_ids = [genre.id for genre in self.genres]
        query = ' '.join([
            'SELECT DISTINCT bg.book_id',
            'FROM {} bg'.format(BookGenre.__table__),
            'WHERE bg.id in ({})'.format(self._get_genre_query_string())
        ])
        rows = db.engine.execute(query)
        allowed_book_ids = [row['book_id'] for row in rows]

        filtered_results = []
        for result in results:
            if (result.book.id in allowed_book_ids):
                filtered_results.append(result)

        return filtered_results
            
    def _build_query(self):
        order_by = 'total_score DESC'
        if self.order_by == 'score':
            order_by = 'total_score DESC'
        elif self.order_by == 'rating':
            order_by = 'b.rating DESC'
            
        query = ' '.join([
            'SELECT b.id, b.isbn, b.isbn13, b.title, b.author, b.price, b.rating, b.description, b.cover_image_url, b.goodreads_url, b.goodreads_author_url, b.amazon_url, b.created_at, b.updated_at, SUM(bm.score) / {} AS total_score'.format(len(self.moods)),
            'FROM {} bm, {} b'.format(BookMood.__table__, Book.__table__),
            'WHERE bm.mood_id in ({})'.format(self._get_mood_query_string()),
            'AND bm.book_id = b.id',
            'GROUP BY b.id, b.isbn, b.isbn13, b.title, b.author, b.price, b.rating, b.description, b.cover_image_url, b.goodreads_url, b.goodreads_author_url, b.amazon_url, b.created_at, b.updated_at',
            'HAVING total_score > {}'.format(self.min_score),
            'ORDER BY {}'.format(order_by),
            'LIMIT {}'.format(self.limit)
        ])

        return query


    def _get_mood_query_string(self):
        moods = self.moods
        return ','.join(['{}'.format(mood.id) for mood in moods])

    def _get_genre_query_string(self):
        genres = self.genres
        return ','.join(['{}'.format(genre.id) for genre in genres])

    def _make_query_result(self, row):
        return SearchQueryResult(row['total_score'], Book(row))

