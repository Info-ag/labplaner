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

    def get(self, uid=None, firstname=None, lastname=None, mail=None, password=None, birthday=None, pgids=None, isadmin=None, ismentor=None, ismember=None):
        '''Search for user datas that fits to the values.'''

        if uid:
            return self.users.select().where(self.users.c.uid == uid).execute().fetchone()
        elif firstname:
            return self.users.select().where(self.users.c.firstname == firstname).execute().fetchall()
        elif lastname:
            return self.users.select().where(self.users.c.lastname == lastname).execute().fetchall()
        elif mail:
            return self.users.select().where(self.users.c.mail == mail).execute().fetchall()
        elif password:
            return self.users.select().where(self.users.c.password == password).execute().fetchall()
        elif birthday:
            return self.users.select().where(self.users.c.birthday == birthday).execute().fetchall()
        elif pgids:
            return self.users.select().where(self.users.c.pgids == pgids).execute().fetchall()
        elif isadmin:
            return self.users.select().where(self.users.c.isadmin == isadmin).execute().fetchall()
        elif ismentor:
            return self.users.select().where(self.users.c.ismentor == firstname).execute().fetchall()
        elif ismember:
            return self.users.select().where(self.users.c.ismember == ismember).execute().fetchall()

    def get_all(self):
        '''Search for all user datas.'''

        return self.users.select().execute().fetchall()

    def patch(self, uid, name, value):
        '''Updates data of a user.'''

        if name == 'firstname':
            return self.users.select().where(self.users.c.uid == uid).execute(firstname=value)
        elif name == 'lastname':
            return self.users.select().where(self.users.c.uid == uid).execute(lastname=value)
        elif name == 'mail':
            return self.users.select().where(self.users.c.uid == uid).execute(mail=value)
        elif name == 'password':
            return self.users.select().where(self.users.c.uid == uid).execute(password=value)
        elif name == 'birthday':
            return self.users.select().where(self.users.c.uid == uid).execute(birthday=value)
        elif name == 'pgids':
            return self.users.select().where(self.users.c.uid == uid).execute(pgids=value)
        elif name == 'isadmin':
            return self.users.select().where(self.users.c.uid == uid).execute(isadmin=value)
        elif name == 'ismentor':
            return self.users.select().where(self.users.c.uid == uid).execute(ismentor=value)
        elif name == 'ismember':
            return self.users.select().where(self.users.c.uid == uid).execute(ismember=value)

    def delete(self, uid):
        '''Deletes a user from database.'''

        return self.user.delete().where(self.users.c.uid == uid).execute().fetchall()



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


class APIS(Database):

    def __init__(self):
        super().__init__()
        self.load()

    def create(self):
        '''Creates the default table for api data.'''

        self.apis = Table('apis', self.metadata,
            Column('aid', Integer, primary_key=True),
            Column('client_id', String(20)), #TODO Ideal String lengths
            Column('secret_key', String(15)),
            Column('level', Integer),
            )
        self.apis.create()

    def load(self):
        '''Loads all apis data.'''

        try:
            self.users = Table('apis', self.metadata, autoload=True)
        except exc.NoSuchTableError:
            self.create()


    def add(self, client_id, secret_key, level):
        '''Creates a new apis.'''

        insert = self.apis.insert()
        insert.execute(client_id=client_id, secret_key=secret_key, level=level)

    def get(self, client_id, secret_key):
        '''Return data if client exist, else None.'''

        return self.apis.select().where(and_(self.apis.c.client_id == client_id, self.apis.c.secret_key == secret_key).execute().fetchone())


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
