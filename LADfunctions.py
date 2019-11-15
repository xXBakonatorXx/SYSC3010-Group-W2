#Database functions
#This script is designed to perform tasks on the SQLite3 database tables
import json
import sqlite3

class LAD_Functions():
#This function converts a JSON file into a readable Python dictionary    
    def json_to_dict(file):
        with open(file, 'r') as f:
            jsonDict = json.load(f) #load the file into our new dictionary
        return jsonDict

    #
    def sql_to_json(table):
        def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        #open connection
        conn = sqlite3.connect('test3.sqlite')
        cursor = conn.cursor()
        #define query we want to make 
        query = "SELECT * FROM '%s'" % jsonDict.keys() #todo: workout how to define which table we are reading from
        cursor.execute(query)    
        #close the connection
        conn.commit()
        conn.close()
        #todo: finish this
        
    #Insert any number of rows from json file to sql database 
    def insert_row(jsonfile):
        jsonDict = json_to_dict(jsonfile)
        tablename = jsonDict.keys()
        if (tablename = 'items'):
            for keys, info in jsonDict:
                query = "INSERT INTO items (name, location) VALUES ('%s', '%s')" %
                for keys in info:
                    info[key]
        else if (tablename = 'locations'):
            for keys, info in jsonDict:
                query = "INSERT INTO items (name, location) VALUES ('%s', '%s')" %
                for keys in info:
                    info[key] 

