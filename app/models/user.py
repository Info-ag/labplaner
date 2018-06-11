import secrets
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy.sql import exists, and_

from app import app, ma, db
from app.models.ag import AGSchema, AG
from app.models.associations import UserAG 
from app.models.date import DateSchema


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(48), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    all_ags = db.relationship('AG', secondary='users_ags')
    ags = db.relationship('AG', secondary='users_ags', primaryjoin=and_(id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role != "NONE"))
    invites = db.relationship('AG', secondary='users_ags', primaryjoin=and_(id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.status == "INVITED"))
    dates = db.relationship('Date', secondary='users_dates')
    sessions = db.relationship('Session')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)


class UserSchema(ma.Schema):
    ags = ma.Nested(AGSchema, many=True, exclude=('users',))
    dates = ma.Nested(DateSchema, many=True, exclude=('user',))
    picture = ma.Method('get_picture_for_user')
    ag_role = ma.Method('get_role_for_ag')

    def get_picture_for_user(self, obj: User):
        return 'https://www.gravatar.com/avatar/' + hashlib.md5(obj.email.lower().encode()).hexdigest() + '?d=mm'

    def get_role_for_ag(self, obj: User):
        ag_id = self.context.get('ag_id')
        if ag_id and db.session.query(exists().where(UserAG.user_id == obj.id and UserAG.ag_id == ag_id)).scalar():
            user_ag: UserAG = UserAG.query.filter_by(user_id=obj.id, ag_id=ag_id).scalar()
            return user_ag.role
        else:
            return 'NONE'

    class Meta:
        fields = ('id', 'username', 'ags', 'picture', 'ag_role', 'dates')


class UserSchemaSelf(UserSchema):
    class Meta:
        fields = ('id', 'username', 'ags', 'picture', 'ag_role', 'email')


class UserSchemaDates(ma.Schema):
    dates = ma.Nested(DateSchema, many=True, exclude=('user',))

    class Meta:
        fields = ('dates',)


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expires = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(64), nullable=False)
    public_token = db.Column(db.String(16), unique=True, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    revoked = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user: User = None, days=60):
        if user:
            self.user_id = user.id
            self.authenticated = True
        else:
            self.user_id = None
            self.authenticated = False

        self.token = secrets.token_hex(64)
        self.public_token = secrets.token_hex(16)
        self.expires = datetime.today() + timedelta(days=days)

    def get_string_cookie(self):
        '''
        Generate a custom string cookie that includes both the public as well as the private token.
        :return: Cookie string
        '''
        dig = hmac.new(app.secret_key, msg=self.token.encode('utf-8'), digestmod=hashlib.sha256).digest()
        str_dig = base64.b64encode(dig).decode()
        return f'{self.public_token}+{str_dig}'

    @staticmethod
    def verify(cookie: str):
        '''
        Check if the provided cookie is part of a valid session.
        :param cookie: String cookie: 'public_token+hash(token)'
        :return: a Session object when the session cookie was valid, False if
            the session cookie was invalid
        '''
        if cookie:
            # get public token from cookie string
            pub = cookie.split('+')[0]
            # check if a session with the public token exists
            if db.session.query(exists().where(Session.public_token == pub)).scalar():
                # get the session from the db
                session = Session.query.filter_by(public_token=pub).scalar()
                if session.expires > datetime.now() and not session.revoked:
                    if secrets.compare_digest(session.get_string_cookie(), cookie):
                        return session

        return False


    def __repr__(self):
        return f'<Session {self.id}>'
