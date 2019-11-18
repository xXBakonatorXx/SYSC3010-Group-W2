#Database functions
#This script is designed to perform tasks on the SQLite3 database tables
import json
import sqlite3

class LAD_Functions(self):
#This function converts a JSON file into a readable Python dictionary    
    def json_to_dict(self, file):
        with open(file, 'r') as f:
            jsonDict = json.load(f) #load the file into our new dictionary
        return jsonDict

    #
    def sql_to_json(self, table):
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
    # This works for single rows, to make multiple, call it many times per entry in json dict  
    def insert_row(self, jsonfile): #todo: check primary key 
        conn = sqlite3.connect('test3.sqlite')
        cursor = conn.cursor(); 
        #turn json to dict
        jsonDict = json_to_dict(jsonfile)
        #table name is just the first key in our nested dict
        tablename = jsonDict.keys()
        if tablename is None:
            raise TypeError("table not specified")
        try:
            if (tablename == 'items'):
                #since it's nested, we have to iterate through both dicts
                queryList = []
                for keys, info in jsonDict:
                    for keys in info:
                        if info[keys] is None:
                            raise TypeError("null fields not allowed")
                        cursor.execute("SELECT COUNT(1) FROM %s WHERE unique_key = %s" % (tablename, items[keys]))
                    queryList.append(info[keys])
                query = "INSERT INTO items (name, location) VALUES ('%s', '%s');" % (queryList[0], queryList[1])
                cursor.execute(query)
              
            elif (tablename == 'locations'):
                queryList = []
                for keys, info in jsonDict:
                    for keys in info:
                        if info[keys] is None:
                            raise TypeError("null fields not allowed")
                    queryList.append(info[keys])
                for keys, info in jsonDict:
                    query = "INSERT INTO locations (name, PathA, PathB, PathC, PathD) VALUES ('%s', '%s', '%s', '%s', '%s');" % (queryList[0], queryList[1], queryList[2], queryList[3], queryList[4])
            cursor.execute(query)
        except NoName: 
            raise Exception("name error")
        except: 
            print("Oops, something went wrong")
        finally: 
            cursor.commit()
            cursor.close()


    #to delete a row with a specific name 
    def delete_row(self, tableName, name):
        conn = sqlite3.connect('test3.sqlite')
        cursor = conn.cursor()
        try:
            query = "DELETE FROM %s WHERE name = %s;" % tableName, name 
            cursor.execute(query)
        except:
            print("oops, something went wrong")
        finally: 
            cursor.commit()
            cursor.close()

    #

    

