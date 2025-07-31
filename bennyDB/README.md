# BennyDB
db 4 benny 

This is a SQLite3 database stored on local device. To use in a program:

1. "import sqlite3"
2. "import db_connector_real"
3. In the same folder as the db_connector_real.py file, create a database file called "BennyDB.sqlite3"
4. For ease of testing, I recommend installing a SQLite3 Editor extension on your IDE. SQLite files are not quite human-readable.
5. Dates must be passed as strings in "%m/%d/%Y" format.

DB is locally stored, requests shouldn't be necessary. You can call database manipulation functions directly from your main program.
DB manipulation functions that get should output in lists of tuples. 
