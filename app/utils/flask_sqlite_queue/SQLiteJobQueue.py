
import os
import sqlite3 
import pickle
import datetime
import threading
import time
import warnings

from .SQLiteJob import SQLiteJob
from .NotAJobTypeWarning import NotAJobTypeWarning

def _get_con(path):
    return sqlite3.Connection(path, 
                    timeout=60)

def _create_database(con, table):
    query = '''
        CREATE TABLE IF NOT EXISTS {} 
        (
            id          INTEGER    PRIMARY KEY AUTOINCREMENT,
            job         BLOB       NOT NULL                 ,
            deadline    DATETIME   NOT NULL                 , 
            started_at  DATETIME                            ,
            finished_at DATETIME                            ,
            created_at  DATETIME   DEFAULT CURRENT_TIMESTAMP,                    
            updated_at  DATETIME   DEFAULT CURRENT_TIMESTAMP 
        )
        '''.format(table)

    con.execute(query)
    con.commit()

def _schedule_job(con, table, job, deadline):
    query = '''
        INSERT INTO {} (job, deadline) VALUES (?, ?)
    '''.format(table)
    
    con.execute(query, [job, deadline])
    con.commit()

def _get_due_jobs(con, table):
    query = '''
        SELECT id, job
        FROM {}
        WHERE deadline < ?
        AND started_at IS NULL
        ORDER BY deadline ASC
    '''.format(table)

    cursor = con.execute(query, [datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")])
    return [(row[0], row[1]) for row in cursor.fetchall()]

def _get_future_jobs(con, table):
    query = '''
        SELECT id, job
        FROM {}
        WHERE deadline > ?
        ORDER BY deadline ASC
    '''.format(table)

    cursor = con.execute(query, [datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")])
    return [(row[0], row[1]) for row in cursor.fetchall()]

def _start_job(con, table, id):
    query = '''
        UPDATE {}
        SET started_at = ?, updated_at = ?
        WHERE id = ?
    '''.format(table)

    con.execute(query, [
        datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
        datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        id])
    con.commit()

def _finish_job(con, table, id):
    query = '''
        UPDATE {}
        SET finished_at = ?, updated_at = ?
        WHERE id = ?
    '''.format(table)

    con.execute(query, [
        datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
        datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        id])
    con.commit()

def _clean_table(con, table, id):
    query = '''
        DELETE FROM {}
        WHERE finished_at IS NOT NULL
    '''.format(table)

    con.execute(query)
    con.commit()

class SQLiteJobQueue(object):

    def __init__(self, path, table = 'queue', max_workers = 5):
        self.path = os.path.abspath(path)
        self.table = table
        self.max_workers = max_workers
        self.workers = []
        self._due_jobs = []
        self._job_lock = threading.Lock()
        self._worker_threads = {}

        with _get_con(self.path) as con:
            # create database if necessary
            _create_database(con, self.table)

    def run(self, job):
        ''' Runs a job in th next cycle '''
        self.delay(job, 0)

    def delay(self, job, seconds):
        ''' Takes a SQLiteJob and runs it after seconds '''
        deadline = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        self.schedule(job, deadline)

    def schedule(self, job, deadline):
        if not isinstance(job, SQLiteJob):
            ''' Takes a SQLiteJob and runs it at a specified deadline '''
            warnings.warn('Expected {}. Received {}. This call will be ignored.'.format(SQLiteJob, type(job)), NotAJobTypeWarning)
            return

        job_dump = pickle.dumps(job)
        date_string = deadline.strftime("%Y-%m-%d %H:%M:%S")

        with _get_con(self.path) as con:
            _schedule_job(con, self.table, job_dump, date_string)

    def run_due_jobs(self):
        self._load_due_jobs()
        self._spawn_worker_threads()

    def get_future_jobs(self):
        future_jobs = []
        with _get_con(self.path) as con:
            queue = _get_future_jobs(con, self.table)

            for (id, job_dump) in queue:
                job = pickle.loads(job_dump)
                job.id = id
                future_jobs.append(job)
        return future_jobs

    def _load_due_jobs(self):
        with self._job_lock:
            queue = []
            with _get_con(self.path) as con:
                queue = _get_due_jobs(con, self.table)

            self._due_jobs = []
            for (id, job_dump) in queue:
                job = pickle.loads(job_dump)
                job.id = id
                self._due_jobs.append(job)

    def _spawn_worker_threads(self):
        ids_to_remove = []
        for key, thread in self._worker_threads.items():
            if not thread.is_alive():
                ids_to_remove.append(key)
        
        for key in ids_to_remove:
            self._worker_threads.pop(key)

        create_new_threads = self.max_workers - len(self._worker_threads.items())

        if create_new_threads > 0:
            for i in range(0,create_new_threads):
                t = threading.Thread(target=self._run_job)
                t.daemon = True
                t.start()
                self._worker_threads[id(t)] = t
        
               
    def _run_job(self):
        job = None
        with self._job_lock:
            if len(self._due_jobs):
                job = self._due_jobs.pop(0)

        if job is None:
            # exit the thread
            return

        with _get_con(self.path) as con:
            _start_job(con, self.table, job.id)
            job.run()
            _finish_job(con, self.table, job.id)

        if len(self._due_jobs):
            self._run_job()
