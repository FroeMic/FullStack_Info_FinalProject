# Usage

You can either use this script directly from the command line or from using python.
In both cases make sure that the database schema is set up according to the configuration.

**1. CLI Usage**

```
python import_books.py -d ../../../app/data/app.db -i ./book_import_example.csv --seperator ';'
```

**2.  Python Interative Shell**

[1] Run `python` to bring up the interactive shell.

[2] Import the script
```
import import_books as ip
```

[3] Configure the script. Be sure to set at least the `DB_PATH` and the `INPUT_FILE` path.
```
ip.DB_PATH = '../../../app/data/app.db'
ip.INPUT_FILE = './book_import_example.csv'
```

[4] Configure any other configu variables if neccessary (optional)

- `INPUT_FILE_SEPERATOR`
- `DB_BOOK_TABLE`
- `DB_MOOD_TABLE`
- `DB_BOOK_MOOD_TABLE`
- `DB_ISBN_COLUMN`
- `DB_ISBN13_COLUMN`
- `DB_MOOD_COLUMN`
- `DB_PIVOT_MOOD_ID_COLUMN`
- `DB_PIVOT_BOOK_ID_COLUMN`
- `DB_PIVOT_SCORE_COLUMN`
- `INPUT_ISBN_COLUMN`
- `INPUT_ISBN13_COLUMN`
- `INPUT_IGNORE_COLUMNS`

[5] Run the input script

```
ip.run()
```