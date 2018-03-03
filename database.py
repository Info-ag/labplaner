from sqlite3 import connect

class Database(object):

    def __init__(self):

        self.connection = connect('data.db')
