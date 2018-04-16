from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'


# Configure queue
from app.utils.flask_sqlite_queue import Job, create_queue, configure_scheduler
# If flask is run with the `use_reloader` set to True
# the queue will be spawned to times. 
# Be sure to disable this flag for production deployment.
# app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'], use_reloader=True)

configure_scheduler(cycle_interval=30.0) #scheduler checks every 30 seconds
queue = create_queue(app.config['JOB_QUEUE_DATABASE_URI'])

from app import routes, models, forms, utils, tasks

goodreadsjob = tasks.SyncBooksWithGoodReadsJob()
queue.run(goodreadsjob) # runs the job immediately

def _create_database():
    ''' Creates the database schema specified by the SQLAlchemy models '''
    print('Rebuilding database schema ... ')
    db.create_all()
    print('Done!')