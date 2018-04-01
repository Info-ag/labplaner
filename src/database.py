#pylint: disable-all
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Boolean, Date, exc, and_
from configparser import ConfigParser
from hashlib import sha256

class Database(object):

    def __init__(self):

        self.config = Configuration()
        self.load_database()

    def load_database(self):
        '''Loads a MySQL/MariaDB database with the data in config.ini'''

        self.database = create_engine('mysql://%s:%s@%s:%s/%s' % (self.config.user, self.config.password, self.config.host, self.config.port, self.config.database))
        self.database.echo = False
        self.metadata = MetaData(self.database)


class User(Database):

    def __init__(self):
        super().__init__()
        self.load()

    def create(self):
        '''Creates the default table for user data.'''

        self.users = Table('users', self.metadata,
            Column('uid', Integer, primary_key=True),
            Column('firstname', String(15)), #TODO Ideal String lengths
            Column('lastname', String(15)),
            Column('mail', String(35)),
            Column('password', String(20)),
            Column('birthday', String(10)),  #TODO Change this to Date ?
            Column('pgids', Integer),    #TODO Add multiple AG support
            Column('isadmin', Boolean),
            Column('ismentor', Boolean),
            Column('ismember', Boolean),
            )
        self.users.create()

    def load(self):
        '''Loads all user data.'''

        try:
            self.users = Table('users', self.metadata, autoload=True)
        except exc.NoSuchTableError:
            self.create()


    def add(self, firstname, lastname, mail, password, birthday, pgids, ismentor, ismember, isadmin=False):
        '''Creates a new user.'''

        insert = self.users.insert()
        insert.execute(firstname=firstname, lastname=lastname, mail=mail, password=password, birthday=birthday, pgids=pgids, isadmin=isadmin, ismentor=ismentor, ismember=ismember)
        return 'Added successfully %s %s' % (firstname, lastname)

    def get_password(self, firstname, lastname):
        '''Search for the password of a given user.'''

        select = self.users.select().where(and_(self.users.c.firstname == firstname, self.users.c.lastname == lastname))
        rowselected = select.execute()
        for row in rowselected:
            return row.password


class ProjectGroup(Database):

    def __init__(self):
        super().__init__()
        self.load()

    def create(self):
        '''Creates the default table for project group data.'''

        self.ags = Table('projectgroups', self.metadata,
            Column('pgid', Integer, primary_key=True),
            Column('name', String(20)),
            Column('uids', String(30)),     #TODO Add multiple User support
            Column('mentoruids', Integer),
            Column('memberuids', Integer),
            )
        self.ags.create()

    def load(self):
        '''Loads all project group data.'''

        try:
            self.ags = Table('projectgroups', self.metadata, autoload=True)
        except exc.NoSuchTableError:
            self.create()


class Dates(Database):

    def __init__(self):
        super().__init__()
        self.load()

    def create(self):
        '''Creates the default table for project group data.'''

        self.dates = Table('dates', self.metadata,
            Column('dateid', Integer, primary_key=True),  #TODO Create dates table structure
            )
        self.dates.create()

    def load(self):
        '''Loads all dates data.'''

        try:
            self.dates = Table('dates', self.metadata, autoload=True)
        except exc.NoSuchTableError:
            self.create()

    def add_column(self):
        '''Add column to dates data.'''

        column = Column('new column', String(100), primary_key=True)
        column_name = column.compile(dialect=engine.dialect)
        column_type = column.type.compile(engine.dialect)
        self.database.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


class Configuration(object):

    def __init__(self):
        self.config_file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_file)

    @property
    def user(self):
        return self.config['Credentials']['User']

    @user.setter
    def user(self, value):
        self.config['Credentials']['User'] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    @property
    def password(self):
        return str(self.config['Credentials']['Password'])

    @password.setter
    def password(self, value):
        self.config['Credentials']['Password'] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    @property
    def database(self):
        return self.config['Credentials']['Database']

    @database.setter
    def database(self, value):
        self.config['Credentials']['Database'] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    @property
    def host(self):
        return self.config['Credentials']['Host']

    @host.setter
    def host(self, value):
        self.config['Credentials']['Host'] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    @property
    def port(self):
        return int(self.config['Credentials']['Port'])

    @port.setter
    def port(self, value):
        self.config['Credentials']['Port'] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)


if __name__ == '__main__':
    pass
