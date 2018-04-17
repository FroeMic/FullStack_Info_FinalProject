import sys
import os
import getopt
import termcolor

from datetime import datetime

import sqlite3 as sql
import pandas as pd
import numpy as np


# CONFIG
# =============
DB_PATH = None
INPUT_FILE =  None
INPUT_FILE_SEPERATOR = ';'

DB_BOOK_TABLE = 'book'
DB_MOOD_TABLE = 'mood'
DB_BOOK_MOOD_TABLE = 'book_mood'

DB_ISBN_COLUMN = 'isbn'
DB_ISBN13_COLUMN = 'isbn13'
DB_MOOD_COLUMN = 'title'
DB_PIVOT_MOOD_ID_COLUMN = 'mood_id'
DB_PIVOT_BOOK_ID_COLUMN = 'book_id'
DB_PIVOT_SCORE_COLUMN = 'score'

INPUT_ISBN_COLUMN = 'isbn'
INPUT_ISBN13_COLUMN = 'isbn13'
INPUT_IGNORE_COLUMNS = [ 'book_title' ]

# ===========
# CLI helpers
# ===========
def parse_arguments():
    ''' Parses the command line arguments and fills the config variables '''
    global DB_PATH
    global INPUT_FILE
    global INPUT_FILE_SEPERATOR

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:i:s:",["help"])
    except getopt.GetoptError:
        print_usage_and_exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage_and_exit()
        elif opt in ('-d'):
            DB_PATH = arg
        elif opt in ('-i'):
            INPUT_FILE = arg
        elif opt in ('-s'):
            INPUT_FILE_SEPERATOR = arg

    if not all([DB_PATH, INPUT_FILE]):
        print_usage_and_exit()

def print_usage_and_exit():
    ''' Prints a short message on how to use the cli interface '''
    log_error('Usage: ' + sys.argv[0] + ' -d <db_path> -i <input_file_path>')
    fatal_error()

def log_error(str):
    ''' Prints a string in red color '''
    print(termcolor.colored(str, 'red'))

def log_warning(str):
    ''' Prints a string in yellow color '''
    print(termcolor.colored(str, 'yellow'))

def log_info(str):
    ''' Prints a string in white color '''
    print(termcolor.colored(str, 'white'))

def fatal_error():
    ''' Exits the program. '''
    log_error('FATAL ERROR! Import Failed.')
    sys.exit(2)

# ===========
# DB Helpers
# ===========
def check_whether_table_exists(tablename):
    ''' Checks whether the specified table exists. '''
    query = '''
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE name = ? AND type = 'table';
    '''

    with sql.connect(DB_PATH) as con: 
        cur = con.cursor()
        cur.execute(query, [tablename])
        return cur.fetchone()[0] == 1

    return False

def get_last_row_id(con):
    ''' Returns the id of the last row inserted into the database. '''
    return con.execute('SELECT last_insert_rowid()').fetchone()[0]

def insert_or_replace_mood(mood_title):
    ''' Inserts mood_title into the database and returns its row id.'''

    subquery = '''
        SELECT `id` FROM `{}` WHERE `{}`= "{}"
    '''.format(DB_MOOD_TABLE, DB_MOOD_COLUMN, mood_title)

    query = '''
        INSERT OR REPLACE INTO `{}` (`id`, `{}`, `created_at`, `updated_at`)  
        VALUES (({}), ?,?,?)
    '''.format(DB_MOOD_TABLE, DB_MOOD_COLUMN, subquery)

    with sql.connect(DB_PATH) as con: 
        con.execute(query, [
            mood_title,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ])
        con.commit()

        id = get_last_row_id(con)
        return id
        
    return None

def insert_or_replace_book(isbn, isbn13):
    ''' Inserts a book into the database and returns its id. '''

    isbn = str(isbn).zfill(10)
    isbn13 = str(isbn13).zfill(13)
    
    subquery = '''
        SELECT `id` FROM `{}` WHERE `{}`= "{}"
    '''.format(DB_BOOK_TABLE, DB_ISBN13_COLUMN, isbn13)

    query = '''
        INSERT OR REPLACE INTO `{}` (`id`, `{}`, `{}`, `created_at`, `updated_at`)  
        VALUES (({}), ?,?,?,?)
    '''.format(DB_BOOK_TABLE, DB_ISBN_COLUMN, DB_ISBN13_COLUMN, subquery)

    with sql.connect(DB_PATH) as con: 
        con.execute(query, [
            isbn,
            isbn13,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ])
        con.commit()

        id = get_last_row_id(con)
        return id
        
    return None

def insert_or_replace_book_mood_score(book_id, mood_id, score):
    ''' Inserts or replaces a score for a mood, book tuple '''
    subquery = '''
        SELECT `id` FROM `{}` WHERE `{}`= {} AND `{}`= {}
    '''.format(DB_BOOK_MOOD_TABLE, DB_PIVOT_MOOD_ID_COLUMN, mood_id, DB_PIVOT_BOOK_ID_COLUMN, book_id, )

    query = '''
        INSERT OR REPLACE INTO `{}` (`id`, `{}`, `{}`, `{}`, `created_at`, `updated_at`)  
        VALUES (({}), ?,?,?,?,?)
    '''.format(DB_BOOK_MOOD_TABLE, DB_PIVOT_BOOK_ID_COLUMN, DB_PIVOT_MOOD_ID_COLUMN, DB_PIVOT_SCORE_COLUMN, subquery)

    with sql.connect(DB_PATH) as con: 
        con.execute(query, [
            book_id,
            mood_id,
            score,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ])
        con.commit()

        id = get_last_row_id(con)
        return id
        
    return None


# ===========
# Subroutines
# ===========
def database_exists():
    ''' Returns whether the DB_PATH points to a valid file '''
    return os.path.exists(DB_PATH) and os.path.isfile(DB_PATH)

def input_file_exists():
    ''' Returns whether the INPUT_FILE points to a valid file '''
    return os.path.exists(INPUT_FILE) and os.path.isfile(INPUT_FILE)

def load_input_file():
    '''Loads the input file into a pandas dataframe'''
    return pd.read_csv(INPUT_FILE, sep=INPUT_FILE_SEPERATOR)

def drop_ignored_columns(df):
    '''Removes the columns specified in INPUT_IGNORE_COLUMNS from the dataframe'''
    columns_to_drop = [col for col in INPUT_IGNORE_COLUMNS if col in df.columns]
    return df.drop(columns_to_drop, axis=1)

def check_whether_required_columns_exist(df):
    '''Check whether all required columns exist'''
    fatal = False
    if not INPUT_ISBN_COLUMN:
        log_error('Required column "' + INPUT_ISBN_COLUMN + '" is missing in the input file.')
        fatal = True
    if not INPUT_ISBN13_COLUMN:
        log_error('Required column "' + INPUT_ISBN13_COLUMN + '" is missing in the input file.')
        fatal = True

    if fatal:
        fatal_error()

def drop_duplicate_rows(df):
    ''' Removes duplicate rows based on INPUT_ISBN_COLUMN and INPUT_ISBN13_COLUMN columns '''
    df_unique = df.drop_duplicates(subset = [INPUT_ISBN_COLUMN])
    df_unique = df.drop_duplicates(subset = [INPUT_ISBN13_COLUMN])
    number_of_removed_columns = len(df) - len(df_unique)
    if (number_of_removed_columns > 0):
        log_warning('Removed ' + str(number_of_removed_columns) + ' duplicate rows.')
    return df_unique

def get_mood_labels(df):
    ''' Returns a dictionary of all moods that should be inserted into the db. ''' 
    not_mood_columns = [INPUT_ISBN13_COLUMN, INPUT_ISBN_COLUMN] + INPUT_IGNORE_COLUMNS
    return [{'mood_title': col, 'id': None} for col in df.columns if col not in not_mood_columns]

def check_whether_required_tables_exist():
    ''' Checks whether the required tables exit in the database ''' 
    tables = [
        DB_BOOK_TABLE,
        DB_MOOD_TABLE,
        DB_BOOK_MOOD_TABLE
    ]

    for table in tables:
        fatal = False
        if not check_whether_table_exists(table):
            log_error('Table "' + table + '" does not exist in database.')
            fatal = True
        
    if fatal:
        fatal_error()

def add_moods_to_database(moods):
    ''' Adds the an array of [{mood_title: String, id: Any}] to 
    the database and return the sam array with filled in ids'''
    result = []
    for mood in moods:
        id = insert_or_replace_mood(mood['mood_title'])
        if id is not None:
            mood['id'] = id
            result.append(mood)
        else:
            log_warning('Could not insert mood "' + mood['mood_title'] + '"')
    return result

def add_book_to_database(isbn, isbn13, mood_scores):
    ''' Adds the isbn and isbn13 to the db and then all [(mood_id, score)] into the DB_BOOK_MOOD_TABLE table '''
    book_id = insert_or_replace_book(isbn, isbn13)
    if book_id is None:
        log_error('Could not insert book "' + str(isbn13).zfill(13) + '"')
    else:
        for (mood_id, score) in mood_scores:
            insert_or_replace_book_mood_score(book_id, mood_id, score)
            
    
def add_books_to_database(df, moods):
    ''' Adds all books in the dataframe and all moods to the db '''
    for index, row in df.iterrows():
        mood_scores_for_book = [(mood['id'], row[mood['mood_title']]) for mood in moods if not is_empty(row[mood['mood_title']]) ]
        add_book_to_database(row[INPUT_ISBN_COLUMN], row[INPUT_ISBN13_COLUMN], mood_scores_for_book)

def is_empty(value):
    ''' Returns whether a cell is empty (true) or contains a valid score (false) '''
    x = value
    return (x is None) or (x == '') or (is_float(x) and float(x) == 0.0) or (is_float(x) and np.isnan(float(x)))
    
def is_float(value):
    ''' Checks whether a value can be casted to a float '''
    try:
        float(value)
        return True
    except:
        return False

# ===========
# Main routines
# ===========
def run():
    ''' Runs the import with current configuration'''
    # 1. Check wheter database exists
    if not database_exists():
        log_error('Error: Could not locate database at "' + DB_PATH +'"')
        exit(2)

    # 2. Check whether import file exist
    if not input_file_exists():
        log_error('Error: Could not locate the input file at "' + INPUT_FILE +'"')
        exit(2)

    # 3. Check whether all required columns exist (isbn, isbn13, mood1 ... mood n)
    log_info('Analyzing input file ...')
    df = load_input_file()
    df = drop_ignored_columns(df)
    df = drop_duplicate_rows(df)
    check_whether_required_columns_exist(df)
    moods =  get_mood_labels(df)
    log_info('Input file looks good:')
    log_info('\t-> Found ' + str(len(moods)) + ' moods to import.')
    log_info('\t-> Found ' + str(len(df)) + ' books to import.')

     # 4. Check whether required tables exist (books, mood, book_mood)
    log_info('Checking database connection ...')
    check_whether_required_tables_exist()
    log_info('\t-> Database seems to be OK')

    # 5. Add moods to database and fill in their ids.
    log_info('Adding moods to database ...')
    moods =  add_moods_to_database(moods)
    log_info('\t-> Inserted ' + str(len(moods)) + ' moods into the database.')

    # 5. Add the books and the (mood_id, book_id, score) tuples to the database.
    log_info('Adding books to database ...')
    add_books_to_database(df, moods)
    log_info('\t-> Inserted ' + str(len(df)) + ' books with scores.')


if __name__ == '__main__':
    # 1. Read Config variables
    parse_arguments()

    # 2. Run import script
    run()

    # 3. Exit program
    log_info('Script finished successfully!')


