
from .SQLiteJobQueue import SQLiteJobQueue as Queue
from .Scheduler import Scheduler


_scheduler = None

def get_scheduler():
    global _scheduler
    if not _scheduler:
        _scheduler = Scheduler()
        _scheduler.start()
    return _scheduler

''' Facade to expose the JobQueue '''

def create_queue(path, table = 'queue', max_workers = 5):
    ''' Returns a ready-to-use queue '''
    queue = Queue(path, table = table, max_workers = max_workers)
    get_scheduler().register(queue)
    return queue

def remove_queue(queue):
    ''' Removes a registered queue from the scheduler '''
    get_scheduler().deregister(queue)

def configure_scheduler(cycle_interval = 10):
    '''configures the scheduler'''
    get_scheduler().interval = cycle_interval
