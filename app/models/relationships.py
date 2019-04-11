'''
All database models, whhich associate two other database models
    --> UserAG, EventDate, UserDate, UserAGMessage
All Schemas regarding those database models
    --> UserAGMessageSchema
'''
from datetime import datetime
from app import ma
from app.models import db


class UserAG(db.Model):
    __tablename__ = 'ags_users'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))
    role = db.Column(db.String(11), nullable=False, default='NONE')
    status = db.Column(db.String(11), nullable=False, default='NONE')

    # either 'MENTOR', 'PARTICIPANT' or 'NONE'

    def __repr__(self):
        return f'<UserAG {self.id}>'


class EventDate(db.Model):
    __tablename__ = 'events_dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    date_id = db.Column(db.Integer, db.ForeignKey('dates.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f'<EventDate {self.id}>'


class UserDate(db.Model):
    __tablename__ = 'users_dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    date_id = db.Column(db.Integer, db.ForeignKey('dates.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f'<UserDate {self.id}>'

class UserAGMessage(db.Model):
    __tablename__ = 'users_ag_messages'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('ag_messages.id'))
    read = db.Column(db.Boolean, default=False)
    updated = db.Column(db.DateTime, onupdate=datetime.now())
    user = db.relationship('User')


    def __repr__(self):
        return f'<UserAGMessage {self.id}>'

class UserAGMessageSchema(ma.Schema):
    user = ma.Nested('UserSchema')
    class Meta:
        fields = ('user_id', 'read', 'updated', 'user')


class UserMessage(db.Model):
    __tablename__ = 'users_messages'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    read = db.Column(db.Boolean, default=False)

    user = db.relationship('User')
    message = db.relationship('Message')
