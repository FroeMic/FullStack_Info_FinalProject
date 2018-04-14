from app.utils.flask_sqlite_queue import Job
from app import queue

class SyncBooksWithGoodReadsJob(Job):
    
    def run(self):
        print('START SyncBooksWithGoodReadsJob Job')
        queue.delay(self, 5)
