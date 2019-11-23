#!/usr/bin/env python3
import sqlite3

#some initial data
id = 4
temperature = 0.0
date = '2014-01-05'
#connect to database file
dbconnect = sqlite3.connect("lab4.db")
#If we want to access columns by name we need to set
#row_factory to sqlite3.Row class
dbconnect.row_factory = sqlite3.Row
#now we create a cursor to work with db
cursor = dbconnect.cursor()
for i in range(10):
    #execute insert statement
    id += 1
    temperature += 1.1
    cursor.execute('''insert into temperature values (?, ?, ?)''',
    (id, temperature, date))
dbconnect.commit()
#execute simple select statement
cursor.execute('SELECT * FROM temperature')
#print data
for row in cursor:
    print(row['id'],row['temp'],row['date'] )

# LAB 4 EXERCISE 4 PART

#connect to database file
#dbconnect = sqlite3.connect("lab4.db")

#If we want to access columns by name we need to set
#row_factory to sqlite3.Row class
#dbconnect.row_factory = sqlite3.Row

#now we create a cursor to work with db
cursor = dbconnect.cursor()
#We create a new table named sensorID
createTable = "CREATE TABLE sensorID (sensor, type, zone)"

#Create the table with the mouse object
cursor.execute(createTable)
dbconnect.commit()

#Insert our 5 values:
cursor.execute('''INSERT INTO sensorID values(1, "door", "kitchen")''')
#cursor.execute(insertVal)
insertVal = 'INSERT INTO sensorID values(2, "temperature", "kitchen")'
cursor.execute(insertVal)
insertVal = 'INSERT INTO sensorID values(3, "door", "garage")'
cursor.execute(insertVal)
insertVal = 'INSERT INTO sensorID values(4, "motion", "garage")'
cursor.execute(insertVal)
insertVal = 'INSERT INTO sensorID values(5, "temperature", "garage")'
cursor.execute(insertVal)
#actually commit to db
dbconnect.commit()

#execute simple select statement
cursor.execute('SELECT * FROM sensorID')

#print data
for row in cursor:
    print(row['sensor'],row['type'],row['zone'])

#close the connection
dbconnect.close()