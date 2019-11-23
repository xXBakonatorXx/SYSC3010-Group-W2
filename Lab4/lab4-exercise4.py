#!/usr/bin/env python3
import sqlite3

#connect to database file
dbconnect = sqlite3.connect("lab4.db")

#If we want to access columns by name we need to set
#row_factory to sqlite3.Row class
#dbconnect.row_factory = sqlite3.Row

#now we create a cursor to work with db
cursor = dbconnect.cursor()
#We create a new table named sensorID
createTable = "CREATE TABLE sensorID(type, zone)"

#Create the table with the mouse object
cursor.execute(createTable)

#Insert our 5 values:
insertVal = "INSERT INTO sensorID values("door", "kitchen")"
cursor.execute(insertVal)
insertVal = "INSERT INTO sensorID values("temperature", "kitchen")"
cursor.execute(insertVal)
insertVal = "INSERT INTO sensorID values("door", "garage")"
cursor.execute(insertVal)
insertVal = "INSERT INTO sensorID values("motion", "garage")"
cursor.execute(insertVal)
insertVal = "INSERT INTO sensorID values("temperature", "garage")"
cursor.execute(insertVal)
#actually commit to db
dbconnect.commit()

#execute simple select statement
cursor.execute('SELECT * FROM sensorID')

#print data
for row in cursor:
    print(row['type'],row['zone'])

#close the connection
dbconnect.close()