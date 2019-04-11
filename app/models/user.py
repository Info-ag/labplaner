'''
All Database models regarding Users
    --> User, Session
All Marshmallow Schemas regarding those models
    --> UserSchemaSelf, UserSchema, UserSchemaDates
'''



import secrets
import hashlib
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy.sql import exists, and_

from app import ma
from app.models import db
from app.models.ag import AGSchema, AG
from app.models.associations import UserAG
from app.models.date import DateSchema


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(48), unique=True, nullable=True)
    password = db.Column(db.LargeBinary, nullable=False)
    guest = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmation_token = db.Column(db.String(32), nullable=True, unique=True)
    password_token = db.Column(db.String(32), nullable=True, unique=True)

    all_ags = db.relationship('AG', secondary='users_ags')
    ags = db.relationship('AG', secondary='users_ags',
                          primaryjoin=and_(id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role != 'NONE'))
    invites = db.relationship('AG', secondary='users_ags',
                              primaryjoin=and_(id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.status == 'INVITED'))
    dates = db.relationship('Date', secondary='users_dates')
    sessions = db.relationship('Session')

    unread_messages = db.relationship('UserAGMessage', primaryjoin='and_(User.id == UserAGMessage.user_id, UserAGMessage.read == 0)', viewonly=True)

    def __init__(self):
        self.confirmation_token = secrets.token_hex(32)

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
    ag_status = ma.Method('get_status_for_ag')

    def get_picture_for_user(self, obj: User):
        return 'https://www.gravatar.com/avatar/' + hashlib.md5(obj.email.lower().encode()).hexdigest() + '?d=mm'

    def get_role_for_ag(self, obj: User):
        ag_id = self.context.get('ag_id')
        if ag_id and db.session.query(exists().where(UserAG.user_id == obj.id and UserAG.ag_id == ag_id)).scalar():
            user_ag: UserAG = UserAG.query.filter_by(user_id=obj.id, ag_id=ag_id).scalar()
            return user_ag.role
        else:
            return 'NONE'

    def get_status_for_ag(self, obj: User):
        ag_id = self.context.get('ag_id')
        if ag_id and db.session.query(exists().where(UserAG.user_id == obj.id and UserAG.ag_id == ag_id)).scalar():
            user_ag: UserAG = UserAG.query.filter_by(user_id=obj.id, ag_id=ag_id).scalar()
            return user_ag.status
        else:
            return 'NONE'

    class Meta:
        fields = ('id', 'username', 'ags', 'picture', 'ag_role', 'ag_status', 'dates')


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
    session_only = db.Column(db.Boolean, nullable=False, default=True)
    token = db.Column(db.String(64), nullable=False, unique=True)
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
        self.expires = datetime.today() + timedelta(days=days)

    def get_string_cookie(self):
        return f'{self.token}'

    @staticmethod
    def verify(cookie: str):
        if cookie:
            # get public token from cookie string
            # check if a session with the public token exists
            if db.session.query(exists().where(Session.token == cookie)).scalar():
                # get the session from the db
                session = Session.query.filter_by(token=cookie).scalar()
                if session.expires > datetime.now() and not session.revoked:
                    return session

        return False

    def __repr__(self):
        return f'<Session {self.id}>'
