#Database functions
#This script is designed to perform tasks on the SQLite3 database tables
import json
import sqlite3 
import sys
#from mock import recieveData
from to_file import to_file




#Listen on Ports:
#write to ports 



#This function converts a JSON file into a readable Python dictionary    
def json_to_dict(jsonfile):
    with open(jsonfile, 'r') as f:
        data=f.read()#load the file into our new dictionary
    jsonDict = json.loads(data)
    return jsonDict

        
def sql_to_json(table):
    #open connection
    conn = sqlite3.connect('{db}'.format(db = "test3.sqlite"))
    cursor = conn.cursor()
    #define query we want to make 
    query = "SELECT * FROM '%s'" % table 
    cursor.execute(query)
    result = cursor.fetchall()
    print (result)
    #close the connection
    conn.commit()
    conn.close()
    
    return result # returns the formatted JSON. We can use this to send messages and other functions

    
#Insert a row from json file to sql database
# This works for single rows, to make multiple, call it many times per entry in json dict  
def insert_row(cmdList): 
    conn = sqlite3.connect('test3.sqlite')
    cursor = conn.cursor(); 
    #table name is just the first item of our list
    tablename = cmdList[0]
    if tablename is None: #we don't want null values, but we need to catch this before testing the value 
        raise TypeError("table not specified")
    try:
        if (tablename == 'items'):
            cursor.execute("INSERT INTO {tablename} ({colid}, {colname}) VALUES ('{val1}', '{val2}')".\
            format(tablename = 'items', colid = 'name', colname = 'location', val1 = cmdList[2], val2 = cmdList[4]))
            
        elif (tablename == 'locations'): 
            cursor.execute("INSERT INTO locations (name, PathA, PathB, PathC, PathD) VALUES ('{val1}', '{val2}', '{val3}', '{val4}', '{val5}')".\
            format(val1 = cmdList[2], val2 = cmdList[4], val3 = cmdList[6], val4 = cmdList[8], val5 = cmdList[10]))
    except: 
        print('Oops, something went wrong')
    finally: 
        conn.commit()
        conn.close()


#to delete a row with a specific name 
def delete_row(tableName, name):
    conn = sqlite3.connect('{db}'.format(db='test3.sqlite'))
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
    print(json_to_dict('decode.json'))       

if __name__ == "__main__":
    main()