import sys
import os
import getopt
import termcolor


# CONFIG
# =============
DB_PATH = None
INPUT_FILE =  None

DB_BOOK_TABLE = 'book'
DB_MOOD_TABLE = 'mood'
DB_BOOK_MOOD_TABLE = 'book_mood'

DB_ISBN_COLUMN = 'isbn'
DB_ISBN13_COLUMN = 'isbn13'
DB_MOOD_COLUMN = 'title'

INPUT_ISBN_COLUMN = 'isbn'
INPUT_ISBN13_COLUMN = 'isbn13'
INPUT_IGNORE_COLUMNS = [ 'title' ]

# ===========
# CLI helpers
# ===========
def parse_arguments():
    ''' Parses the command line arguments and fills the config variables '''
    global DB_PATH
    global INPUT_FILE

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:i:",["help"])
    except getopt.GetoptError:
        print_usage_and_exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage_and_exit()
        elif opt in ('-d'):
             DB_PATH = arg
        elif opt in ('-i'):
             INPUT_FILE = arg

    if not all([DB_PATH, INPUT_FILE]):
        print_usage_and_exit()

def print_usage_and_exit():
    ''' Prints a short message on how to use the cli interface '''
    log_error('Usage: ' + sys.argv[0] + ' -d <db_path> -i <input_file_path>')
    sys.exit(2)

def log_error(str):
    ''' Prints a string in red color '''
    print(termcolor.colored(str, 'red'))

def log_info(str):
    ''' Prints a string in blue color '''
    print(termcolor.colored(str, 'blue'))


# ===========
# Main routines
# ===========
def run():
    ''' Runs the import with current configuration'''
    # 1. Check wheter database exists
    # 2. Check whether required table exist (books, mood, book_mood)
    # 3. Check whether import file exist
    # 4. Check whether all required columns exist (isbn, isbn13, mood1 ... mood n)
        # 4.1 Print log statement
        # Importing x moods
        # Importing x books
        # Skipping x books due to missing isbn or isbn13 values.
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


