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

        selects entries that match condition from table
        and returns a tuple of the data

        >>> database.select("test", '''name=="john smith"''')
        ("john smith", 25)
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
    
    def update(self, update, condition):
        """ (str, str) -> None

        updates an entry in a table
        
        this feature is experimental and not yet inplemented
        """
        return 0

    def close(self):
        """ (None) -> None

        closes the connection to the database
        """
        self.__database__.close()

class JSON:
    def __init__(self, filename):
        self.__filename__ = filename
        self.__data__     = None
        self.read()

    def newTable(self, tablename):
        """ (str) -> None 
        
        adds a new table to the database

        >>> database.newTable('table')
        """



        if tablename in self.__data__.keys():
            print("table already exists")
            return False

        self.__data__[tablename] = list()
        self.__data__[tablename].append(dict())        
        return True

    def removeTable(self, tablename):
        """ (str) -> None 
        
        removes a table to the database

        >>> database.removeTable('table')
        """

        if tablename in self.__data__.keys():
            return self.__data__.pop(tablename)
        
        print("Table {} does not exist".format(tablename))
        return None

    def insert(self, tablename, values):
        """ (str, list) -> None

        adds and entry into a table from a dctionary

        >>> database.insert("table", [val, val, val])
        """
        exist = False
        table = self.__data__[tablename]

        for item in table:
            if item["name"] == values[0]:
                exist = True
                keys = list(item.keys())
                if len(values) == len(keys):
                    for idx in range(len(keys)):
                        item[keys[idx]] = values[idx]
                else:
                    print("invalid number of values")

        if not exist:
            table.append(dict())
            keys = list(table[0].keys())

            if len(values) == len(keys):
                for idx in range(len(keys)):
                    table[-1][keys[idx]] = values[idx]
            else:
                print("invalid number of values")

    def remove(self, tablename, value, result):
        table = self.__data__[tablename]
        remove_items = []
        for item in table:
            if item[value] == result:
                remove_items.append(item)
        
        for item in remove_items:
            table.remove(item)

    def read(self):
        file = open(self.__filename__, 'r')
        self.__data__ = json.load(file)
        file.close()

    def write(self):
        file = open(self.__filename__, "w")
        json.dump(self.__data__, file, indent=4)
        file.close()

    def encode(self):
        return json.dumps(self.__data__)

    def decode(self, datas):
        self.data = json.loads(datas)

    def getData(self):
        return self.__data__

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

def __testJSON__():
    db = JSON("test.json")
    db.removeTable("test")
    db.newTable("test")
    db.remove("branches","name", "zach")
    db.write()

if __name__ == "__main__":
    __testJSON__()
    #__testSQL__()