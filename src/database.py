#pylint: disable-all
from sqlite3 import connect
from os.path import isfile
from hashlib import sha256

class Database(object):

    def __init__(self):

        if not isfile('data.db'):
            self.connection = connect('data.db')
            self.connection.execute('CREATE TABLE user (name TEXT, password TEXT, id TEXT, userid TEXT)')
        else:
            self.connection = connect('data.db')

        def load(self):
            self.data = dict()
            for userset in self.connection.execute('SELECT * FROM user'):
                self.data[userset[0]] = { 'name': userset[0], 'password': userset[1], 'id': userset[2], 'userid': userset[3]}
                return self.data

        def update(self, data):
            self.connection.execute('DELETE TABLE IF EXIST user')
            self.connection.execute('CREATE TABLE user (name TEXT, password TEXT, id TEXT, userid TEXT)')
            data = list()
            for user in self.data:
                data.append((self.data[user]['name'], self.data[user]['password'], self.data[user]['id'], self.data[user]['userid']))
            data = tuple(data)
            self.connection.executemany('INSERT INTO user VALUES(?,?,?,?,?)', data)

if __name__ == '__main__':
    pass
