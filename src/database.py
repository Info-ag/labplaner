#pylint: disable-all
import _mysql as mariadb
from ConfigParser import ConfigParser
from hashlib import sha256

class Database(object):

    def __init__(self):

        self.connection = mariadb.connect(host=Configuration.host(), port=Configuration.port(), user=Configuration.user(), passwd=Configuration.password(),db=Configuration.database())

        

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

class Configuration(object):

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def user(self):
        return self.config['User']

    def password(self):
        return str(self.config['Password'])

    def database(self):
        return self.config['Database']

    def host(self):
        return self.config['Host']

    def port(self):
        return int(self.config['Port'])


if __name__ == '__main__':
    pass
