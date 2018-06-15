'''
Database models regardning AG --> AG, AGMEssage (,Message)
Marshmallow Schema regarding those database models --> AGSchema, AGSchemaIntern, AGMessageSchema
'''

from datetime import datetime
from sqlalchemy import and_
from flask import g
from app import ma
from app.models import db
from app.models.associations import UserAG, UserAGMessage


class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    color = db.Column(db.String())
    # enum: primary, success, dark, warning, error
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)

    users = db.relationship('User', secondary='users_ags', order_by='UserAG.role')

    actual_users = db.relationship('User',\
                                   secondary='users_ags',\
                                   primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role != "NONE")',\
                                   viewonly=True)
    invited_users = db.relationship('User',
                                    secondary='users_ags',\
                                    primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "INVITED")',\
                                    viewonly=True)
    applied_users = db.relationship('User',\
                                    secondary='users_ags',\
                                    primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "APPLIED")',\
                                    viewonly=True)
    mentors = db.relationship('User',\
                              secondary='users_ags',\
                              primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "MENTOR", UserAG.status == "ACTIVE")',\
                              viewonly=True)

    events = db.relationship('Event')

    messages = db.relationship('AGMessage')

    unread_messages = db.relationship('AGMessage',\
                                    secondary='users_ag_messages',\
                                    primaryjoin='and_(UserAGMessage.message_id == AGMessage.id, AG.id == AGMessage.ag_id, UserAGMessage.read == 0, UserAGMessage.user_id == 1)',\
                                    viewonly=True)

    read_messages = db.relationship('AGMessage',\
                                    secondary=f'users_ag_messages',\
                                    primaryjoin=f'and_(UserAGMessage.message_id == AGMessage.id, AG.id == AGMessage.ag_id, UserAGMessage.read == 1, UserAGMessage.user_id == 1)',\
                                    viewonly=True)

    def __repr__(self):
        return f'<AG {self.name}>'


class AGMessage(db.Model):
    __tablename__ = 'ag_messages'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))
    subject = db.Column(db.String(20))
    message = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.now())

    users = db.relationship('UserAGMessage', secondary='users',\
                            primaryjoin='and_(AGMessage.id == UserAGMessage.message_id, UserAGMessage.user_id == User.id)', viewonly=True)

    def __repr__(self):
        return f'<AGMessage {self.id}>'

class AGSchema(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))
    association = ma.Method('get_association', many=True)

    def get_association(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        user_ag = UserAG.query.filter_by(user_id=g.user.id, ag_id=ag_id).scalar()
        return {'role': user_ag.role, 'status': user_ag.status}

    class Meta:
        fields = ('id', 'name', 'display_name', 'description', 'color', 'association')


class AGSchemaIntern(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))
    actual_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    invited_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    applied_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    messages = ma.Nested('AGMessageSchema', many=True)
    read_messages = ma.Method('get_read_messages')
    unread_messages = ma.Method('get_unread_messages')

    def get_unread_messages(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        ag_message = db.session.query(AGMessage).join(UserAGMessage, and_(AGMessage.ag_id == ag_id, UserAGMessage.user_id == g.session.user_id, UserAGMessage.message_id == AGMessage.id, UserAGMessage.read == 0)).all()
        ag_messages_Schema = AGMessageSchema(many=True)
        return ag_messages_Schema.dump(ag_message)

    def get_read_messages(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        ag_message = db.session.query(AGMessage).join(UserAGMessage, and_(AGMessage.ag_id == ag_id, UserAGMessage.user_id == g.session.user_id, UserAGMessage.message_id == AGMessage.id, UserAGMessage.read == 1)).all()
        if len(ag_message) > 1:
            ag_messages_Schema = AGMessageSchema(many=True, exclude=('users',))
        else:
            ag_messages_Schema = AGMessageSchema(many=True, exclude=('users',))
        return ag_messages_Schema.dump(ag_message)


    class Meta:
        fields = (
            'id', 'name', 'display_name', 'description', 'users', 'events', 'color', 'actual_users', 'invited_users',
            'applied_users', 'messages', 'unread_messages', 'read_messages')




class AGMessageSchema(ma.Schema):
    read = ma.Method('get_read_status')
    users = ma.Nested('UserAGMessageSchema', many=True)


    def get_read_status(self, obj: AGMessage):
        if not g.session.authenticated:
            return None
        user_ag_message = db.session.query(UserAGMessage).filter_by(user_id=g.session.user_id, message_id=obj.id).scalar()
        return user_ag_message.read


    class Meta:
        fields = (
            'id', 'ag_id', 'subject', 'message', 'read', 'created', 'users'
        )

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    subject = db.Column(db.String(20))
    message = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.now())


    def __repr__(self):
        return f'<Message {self.id}>'
