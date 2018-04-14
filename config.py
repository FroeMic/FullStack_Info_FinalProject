import os
from dotenv import load_dotenv

# Set basedir
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variable from .env file
# make sure that a .env file with the following variables exists
env_file_path =  os.path.join(basedir, '.env')
load_dotenv(dotenv_path=env_file_path)

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED') != 'False'
SECRET_KEY = os.getenv('SECRET_KEY')

PORT = int(os.getenv('PORT'))
HOST = os.getenv('HOST')

GOODREADS_API_KEY = os.getenv('GOODREADS_API_KEY') 
GOODREADS_API_SECRET = os.getenv('GOODREADS_API_SECRET')

JOB_QUEUE_DATABASE_URI = os.getenv('JOB_QUEUE_DATABASE_URI') 
