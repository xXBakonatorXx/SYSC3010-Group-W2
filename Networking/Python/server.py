from UDPSocket import Server
from Database import Database
import os

PREFIX_LAD = "LAD"
PREFIX_USR = "USR"
 
# Database file
DATABASE   = "sysc3010.db"
ENCODING   = "utf-8"

BRANCH     = "Branches"
OBJECT     = "Objects"

# Codes for sending and receiving
UPDATE     = "update"
INSERT	   = "insert"
DELETE     = "delete"
CONTINUE   = "continue"
EOF        = "***"
   
if __name__ == '__main__':
    server   = Server(1001,ENCODING)
    database = Database(DATABASE)
    
    database.newTable(BRANCH, "name TEXT, pathA INTEGER, pathB TEXT, pathc TEXT, pathD TEXT")
    database.newTable(OBJECT, "name TEXT, location TEXT")

    while (True):
        res, addr, port = server.receive()        
        data_list = res.split("|")

        if data_list[0] == PREFIX_LAD+UPDATE:
            #send database to lad
            command = data_list[0]

        elif data_list[0] == PREFIX_USR+INSERT:
            #insert into database
            command, table, values = data_list

        elif data_list[0] == PREFIX_USR+UPDATE:
            #update and entry
            command, table, condition, values = data_list

        elif data_list[0] == PREFIX_USR+DELETE:
            #delete and entry
            command, table, condition = data_list

        elif data_list[0] == EOF:
            #break loop
            break 
    
    database.close()
    server.close()
    exit(0)