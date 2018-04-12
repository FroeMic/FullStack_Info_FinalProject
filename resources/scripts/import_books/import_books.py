import sys
import os
import getopt
import termcolor
import pandas as pd


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

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:i:s:",["help", "seperator"])
    except getopt.GetoptError:
        print_usage_and_exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage_and_exit()
        elif opt in ('-d'):
             DB_PATH = arg
        elif opt in ('-i'):
             INPUT_FILE = arg
        elif opt in ('-s', '--seperator'):
             INPUT_FILE_SEPERATOR = arg

    if not all([DB_PATH, INPUT_FILE]):
        print_usage_and_exit()

def print_usage_and_exit():
    ''' Prints a short message on how to use the cli interface '''
    log_error('Usage: ' + sys.argv[0] + ' -d <db_path> -i <input_file_path>')
    sys.exit(2)

def log_error(str):
    ''' Prints a string in red color '''
    print(termcolor.colored(str, 'red'))

def log_warning(str):
    ''' Prints a string in yellow color '''
    print(termcolor.colored(str, 'yellow'))


def log_info(str):
    ''' Prints a string in blue color '''
    print(termcolor.colored(str, 'blue'))


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
    if not INPUT_ISBN_COLUMN:
        log_error('Required column "' + INPUT_ISBN_COLUMN + '" is missing in the input file.')
    if not INPUT_ISBN13_COLUMN:
        log_error('Required column "' + INPUT_ISBN13_COLUMN + '" is missing in the input file.')

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
        # 4.1 Print log statement
        # Importing x moods
        # Importing x books
        # Skipping x books due to missing isbn or isbn13 values.

    log_info('Analyzing input file ...')
    df = load_input_file()
    df = drop_ignored_columns(df)
    df = drop_duplicate_rows(df)
    check_whether_required_columns_exist(df)
    moods =  get_mood_labels(df)
    log_info('Input file looks good:')
    log_info('\t-> Found ' + str(len(moods)) + ' moods to import.')
    log_info('\t-> Found ' + str(len(df)) + ' books to import.')

    # print(moods)
    # print(df.head())
    # print(df.columns)

    log_info('Checking database connection ...')

    # 4. Check whether required tables exist (books, mood, book_mood)
    # 5. Check which moods exist in the database by getting their ids
        # 5.1 Print log statement
        # xx moods exits in db already ... skipping
    # 6. Add missing moods and retrieve their ids
        # 6.1 Print log statement
        # Imported xx moods
    # 7. Check which books exist (isbn) in the database and get their ids
        # 7.1 Print log statement
        # xx books exits in db already ... skipping
    # 8. Add missing books and retrieve their ids
        # 8.1 Print log statement
        # Imported xx books
    # 9. Insert or Replace mood_id, book_id, score (see https://stackoverflow.com/questions/3634984/insert-if-not-exists-else-update)
        # 8.1 Print log statement
        # Added xx book_mood scores

   

if __name__ == '__main__':
    # 1. Read Config variables
    parse_arguments()

    # 2. Run import script
    run()

    # 3. Exit program
    log_info('Script finished successfully!')


