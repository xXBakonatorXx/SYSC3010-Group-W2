import sqlite3
import json

class Sqlite3:
    def __init__(self, database):
        self.__database__ = sqlite3.connect(database)
        self.__cursor__   = self.__database__.cursor()
        self.__database__.execute("begin")
    
    def newTable(self, tableName, dataVars):
        """ (str, str) -> None

        creates new sqlite table
        
        >>> database.newtable("test", '''name TEXT, age INTEGER''')
        """
        try:
            self.__cursor__.execute('''CREATE TABLE {} ({})'''.format(tableName, dataVars))
        except:
            print("table {} already exists".format(tableName))
        self.__database__.commit()

    def removeTable(self, tableName):
        """ (str) -> None

        removes sqlite table

        >>> database.remove("test")
        """
        self.__cursor__.execute('''DROP TABLE {}'''.format(tableName))
        self.__database__.commit()

    def insert(self, tableName, values):
        """ (str, str) -> None

        inserts entry into table

        >>> database.insert("test", '''"john smith", 25''')
        """
        self.__cursor__.execute('''INSERT INTO {} VALUES({})'''.format(tableName, values))
        self.__database__.commit()

    def select(self, tableName, condition=None):
        """ (str, str) -> Tuple

        selects entries that match condition from table
        and returns a tuple of the data

        >>> database.select("test", '''name=="john smith"''')
        ("john smith", 25)
        """
        if condition == None:
            self.__cursor__.execute('''SELECT * FROM {}'''.format(tableName))
        else:
            self.__cursor__.execute('''SELECT * FROM {} WHERE {}'''.format(tableName, condition))
        self.__database__.commit()
        return self.__cursor__.fetchall()

    def tables(self):
        """ (None) -> Tuple

        selects tables from database.
        """
        self.__cursor__.execute('''SELECT * FROM sqlite_master WHERE type=="table"''')
        self.__database__.commit()
        return self.__cursor__.fetchall()


    def delete(self, tableName, condition=None):
        """ (str, str) -> None

        deletes entries from table that match condition

        >>> database.select("test", '''name=="john smith"''')
        """
        if condition == None:
            self.__cursor__.execute('''DELETE FROM {}'''.format(tableName))
        else:
            self.__cursor__.execute('''DELETE FROM {} WHERE {}'''.format(tableName, condition))
        self.__database__.commit()
    
    def update(self, tableName, update, condition):
        """ (str, str) -> None

        updates an entry in a table
        
        this feature is experimental and not yet inplemented
        """
        # select tables
        tables = self.tables()        

        for table in tables:
            if tableName == table[1]:


        return 0

    def close(self):
        """ (None) -> None

        closes the connection to the database
        """
        self.__database__.close()

def __testSQL__():
    db = Sqlite3("test.db")
    db.newTable("test", "name Text, value Integer")
    
    db.insert("test", '''"d", 1''')
    db.insert("test", '''"e", 1''')
    db.insert("test", '''"f", 2''')
    db.insert("test", '''"f", 3''')

    data = db.select("test")
    print(data)

    tables = db.tables()
    for table in tables:
        print(table)

    db.removeTable("test")
    db.close()

if __name__ == "__main__":
    __testSQL__()

### TESTED ###
# + newTable
# + insert
# + select
# + tables
# + removeTable
# + close
#
### UNTESTED ###
# - update
# - delete