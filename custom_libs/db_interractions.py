import sqlite3

class dbCon():
    def __init__(self,path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def query(self, q):
        return self.cursor.execute(q)