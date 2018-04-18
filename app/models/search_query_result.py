class SearchQueryResult(object):

    def __init__(self, score, book):
        self.score = float(('%0.2f'%score))
        self.book = book