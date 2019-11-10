#SQLtoJSONround2

import json
import sqlite3

#some setup here
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        
#open connection
conn = sqlite3.connect('test3.sqlite')
cursor = conn.cursor()

query = "SELECT * FROM items"
cursor.execute(query)

results = cursor.fetchall()
with open("datafile.json", "w") as write_file:
    json.dump(results, write_file)
print(results)

#commit, close and pray 
conn.commit()
conn.close()