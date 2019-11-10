import json
import sqlite3

#create a table like this
conn = sqlite3.connect('test3.sqlite')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE `items` (
    `name`  TEXT NOT NULL UNIQUE,
    `location`  TEXT NOT NULL,
    PRIMARY KEY(`name`))'''
);

conn.commit()
conn.close()
