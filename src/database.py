#pylint: disable-all
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Boolean, Date, and_
from configparser import ConfigParser
from hashlib import sha256

class Database(object):

    def __init__(self):

        self.load_database()
        self.load_table_users()
        self.load_table_projectgroups()

    def load_database(self):
        '''Loads a MySQL/MariaDB database with the data in config.ini'''

        self.database = create_engine('mysql://%s:%s@%s:%s/%s' % (Configuration().user, Configuration().password, Configuration().host, Configuration().port, Configuration().database))
        self.database.echo = False
        self.metadata = MetaData(self.database)

    def create_table_users(self):
        '''Creates the default table for user data.'''

        self.users = Table('users', self.metadata,
            Column('uid', Integer, primary_key=True),
            Column('firstname', String),
            Column('lastname', String),
            Column('mail', String),
            Column('password', String),
            Column('birthday', Date),
            Column('pgids', Integer),    #TODO Add multiple AG support
            Column('isadmin', Boolean),
            Column('ismentor', Boolean),
            Column('ismember', Boolean),
            )
        self.users.create()

    def load_table_users(self):
        '''Loads all user data.'''

        self.users = Table('users', metadata, autoload=True)

    def add_user(self, firstname, lastname, mail, password, birthday, pgids, ismentor, ismember, isadmin=False):
        '''Creates a new user.'''

        insert = self.users.insert()
        insert.execute(firstname=firstname, lastname=lastname, mail=mail, password=password, birthday=birthday, pgids=pgids, isadmin=isadmin, ismentor=ismentor, ismember=ismember)
        return 'Added successfully %s %s' % (firstname, lastname)

    def get_user_password(self, firstname, lastname):
        '''Search for the password of a given user.'''

        select = self.users.select().where(_and(self.users.c.firstname == firstname, self.users.c.lastname == lastname))
        rowselected = select.execute()
        for row in rowselected:
            return row.password #TODO The for loop is awkward cause I code it blind

    def create_table_projectgroups(self):
        '''Creates the default table for project group data.'''

        self.ags = Table('projectgroups', self.metadata,
            Column('pgid', Integer, primary_key=True),
            Column('name', String),
            Column('uids', String),     #TODO Add multiple User support
            Column('mentoruids', Integer),
            Column('memberuids', Integer),
            )
        self.ags.create()

    def load_table_projectgroups(self):
        '''Loads all project group data.'''

        self.ags = Table('projectgroups', metadata, autoload=True)

    def create_table_dates(self):
        '''Creates the default table for project group data.'''

        self.dates = Table('dates', self.metadata,
            Column('dateid', Integer, primary_key=True),  #TODO Create dates table structure
            )
        self.dates.create()

    def load_table_dates(self):
        '''Loads all dates data.'''

        self.dates = Table('dates', metadata, autoload=True)

    def add_column_table_dates(self):
        '''Add column to dates data.'''

        column = Column('new column', String(100), primary_key=True)
        column_name = column.compile(dialect=engine.dialect)
        column_type = column.type.compile(engine.dialect)
        self.database.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


class Configuration(object):

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.user = self.duser()
        self.password = self.dpassword()
        self.database = self.ddatabase()
        self.host = self.dhost()
        self.port = self.dport()

    def duser(self):
        return self.config['Credentials']['User']

    def dpassword(self):
        return str(self.config['Credentials']['Password'])

    def ddatabase(self):
        return self.config['Credentials']['Database']

    def dhost(self):
        return self.config['Credentials']['Host']

    def dport(self):
        return int(self.config['Credentials']['Port'])


if __name__ == '__main__':
    pass
