#Database functions
#This script is designed to perform tasks on the SQLite3 database tables
import json
import sqlite3 
import sys
from mock import recieveData


#Listen on Ports:
#write to ports 

def __init__(database):
    self.db = database

#This function converts a JSON file into a readable Python dictionary    
def json_to_dict(jsonfile):
    with open(jsonfile, 'r') as f:
        jsonDict = json.load(f) #load the file into our new dictionary
    return jsonDict

#
def sql_to_json(table):
    def dict_factory(cursor, row):
        d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    #open connection
    conn = sqlite3.connect('{db}'.format(db = database))
    cursor = conn.cursor()
    #define query we want to make 
    query = "SELECT * FROM '%s'" % jsonDict.keys() 
    jsonData = cursor.execute(query)    
    #close the connection
    conn.commit()
    conn.close()
    
    return jsonData # returns the formatted JSON. We can use this to send messages and other functions
    
#Insert any number of rows from json file to sql database
# This works for single rows, to make multiple, call it many times per entry in json dict  
def insert_row( jsonfile): #todo: check primary key 
    conn = sqlite3.connect('{}'.format(db=database))
    cursor = conn.cursor(); 
    #turn json to dict
    jsonDict = json_to_dict(jsonfile)
    #table name is just the first key in our nested dict
    tablename = next(iter(jsonDict))
    if tablename is None:
        raise TypeError("table not specified")
    try:
        if (tablename == 'items'):
            #since it's nested, we have to iterate through both dicts
            for key in jsonDict.items():
                if key is None:
                    raise TypeError("null fields not allowed")
            cursor.execute("INSERT INTO {tablename} ({colid}, {colname}) VALUES ('{val1}', '{val2}')".\
            format(tablename = 'items', colid = 'name', colname = 'location', val1 = jsonDict['items']['name'], val2 = jsonDict['items']['location']))
            
            
        elif (tablename == 'locations'): #this doesn't quite work 
            print(jsonDict['locations']['name'])
            cursor.execute("INSERT INTO locations ({name}, {PathA}, {PathB}, PathC, PathD) VALUES ({val1}, {val2}, {val3}, {val4}, {val5})".\
            format(name = 'name', PathA = 'PathA', PathB = 'PathB', val1 = jsonDict['locations']['name'], val2 = jsonDict['locations']['PathA'], val3 = jsonDict['locations']['PathB'], val4 = jsonDict['locations']['PathC'], val5 = jsonDict['locations']['PathD']))
    except: 
        print("Oops, something went wrong")
    finally: 
        conn.commit()
        conn.close()


#to delete a row with a specific name 
def delete_row(tableName, name):
    conn = sqlite3.connect('{db}'.format(db=database))
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM {tableName} WHERE name = '{criteria}'".\
            format(tableName = tableName, criteria = name))
    
    except:
        print("oops, something went wrong")
    finally: 
        conn.commit()
        conn.close()

def main():
     recieveData(520)  

if __name__ == "__main__":
    main()