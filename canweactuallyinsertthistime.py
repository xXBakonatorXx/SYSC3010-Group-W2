import json
import sqlite3

conn = sqlite3.connect('test3.sqlite')
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO {tablename} ({colid}, {colname}) VALUES ('cup', 'kitchen')".\
                   format(tablename = 'items', colid = 'name', colname = 'location'))
except sqlite3.IntegrityError:
    print('ERROR: ID already exists in PRIMARYKEY{}')
    
conn.commit()
conn.close()