#Database functions
#This script is designed to perform tasks on the SQLite3 database tables
import json
import sqlite3

class LAD_Functions(database name):
#This function converts a JSON file into a readable Python dictionary    def json_to_dict(file):
        with open(file, 'r') as f:
            jsonDict = json.load(f) #load the file into our new dictionary
        jsonList = [] #my empty list
        for x in jsonDict['items']:
            jsonList.append(x['name'])
            jsonList.append(x['location'])
        return jsonList

    #
    def sql_to_json():
        def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        #open connection
        conn = sqlite3.connect('test3.sqlite')
        cursor = conn.cursor()
        #define query we want to make 
        query = "SELECT * FROM items" #todo: workout how to define which table we are reading from
        cursor.execute(query)    
        #close the connection
        conn.commit()
        conn.close()
        #todo: finish this
        
    #Converting the
        

