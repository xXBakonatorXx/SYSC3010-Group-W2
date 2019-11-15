#JSONtoSQLround idk anymore
import sqlite3
import json

#open connection
conn = sqlite3.connect('test3.sqlite')
cursor = conn.cursor()
#now open the json file
with open('datafile.json', 'r') as f:
    testRead_dict = json.load(f) #load file to dictionary
print(testRead_dict) #print for my own sanity
     
List = [] #my empty list
for x in testRead_dict['testItem']:
    List.append(x['name'])
    List.append(x['location'])
print(List[0])
print(List[1])

cursor.execute("INSERT INTO items (name, location) VALUES ('%s', '%s')" % (List[0], List[1]))
conn.commit()
print(cursor.execute('SELECT * FROM items'))
#YEET
conn.close()