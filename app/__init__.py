from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'


# Configure queue
from app.utils.flask_sqlite_queue import Job, create_queue, configure_scheduler, get_future_jobs
# If flask is run with the `use_reloader` set to True
# the queue will be spawned to times. 
# Be sure to disable this flag for production deployment.
# app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'], use_reloader=True)

configure_scheduler(cycle_interval=30.0) #scheduler checks every 30 seconds
queue = create_queue(app.config['JOB_QUEUE_DATABASE_URI'])

from app import routes, models, forms, utils, tasks

def create_database(hard=False):
    ''' Creates the database schema specified by the SQLAlchemy models '''
    if hard:
        drop_database()

    print('Creating database schema ... ')
    try:
        db.create_all()
        print('Done!')
    except Exception as e:
        print('Error! Failed to create database!')
        print('Cleaning up ...')
        os.remove(_get_db_path())
        raise e

def drop_database():
    ''' Drops the current database schema '''
    print('Dropping database schema ... ')
    db.drop_all()
    print('Done!')

def seed_database():
    create_database(hard=True)
    seed.seed_database()

# AUTO SETUP
def _bootstrap_app_if_neccessary():
    db_path = _get_db_path()
    directory_path = '/'.join(db_path.split('/')[:-1])
    _make_sure_directory_exists(directory_path)
    _make_sure_database_exists(db_path)

    should_init_goodreads_sync_job = True
    should_init_amazon_sync_job = True
    for job in get_future_jobs(queue):
        should_init_goodreads_sync_job = should_init_goodreads_sync_job and type(job) != tasks.SyncBooksWithGoodReadsJob
        should_init_amazon_sync_job = should_init_amazon_sync_job and type(job) != tasks.SyncBooksWithAmazonJob

    if should_init_goodreads_sync_job:
        print('Initializing Goodreads API Sync Job ...')
        goodreadsjob = tasks.SyncBooksWithGoodReadsJob()
        queue.run(goodreadsjob) # runs the job immediately      
    
    if should_init_amazon_sync_job:
        print('Initializing Amazon API Sync Job ...')
        amazonjob = tasks.SyncBooksWithAmazonJob()
        queue.run(amazonjob) # runs the job immediately    

def _get_db_path():
    ''' Returns the absolute url of the database '''
    return str(db.engine.url.database)

def _make_sure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def _make_sure_database_exists(path):
    if not os.path.exists(path):
        create_database()

_bootstrap_app_if_neccessary()






