"""Database models regardning AG --> AG, AGMEssage (,Message)
Marshmallow Schema regarding those database models --> AGSchema, AGSchemaIntern, AGMessageSchema
"""

from sqlalchemy import and_
from flask import g
from marshmallow import Schema, Nested, Method

from app.models import db
from app.models.associations import UserAG, UserAGMessage


__all__ = ['AG', 'AGSchema', 'AGSchemaIntern']


class AG(db.Model):
    """AGs are working groups

    Working groups have a number of users related to them. They can have
    different rules such as mentors or students.

    Relationships:
        - `ags_users`
        - `ags_events`
        - `messages`
    """
    __tablename__ = 'ag'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(length=16), unique=True, nullable=False)
    display_name = db.Column(db.String(length=48), unique=True, nullable=False)
    description = db.Column(db.Text(length=140), nullable=True)

    # Always use set_color and get_hex_color
    color = db.Column(db.LargeBinary(length=24))

    users = db.relationship('User', secondary='ags_users',
                            order_by='UserAG.role')

    actual_users = db.relationship(
        'User',
        secondary='ags_users',
        primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role != "NONE")',
        viewonly=True)
    invited_users = db.relationship(
        'User',
        secondary='ags_users',
        primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "INVITED")',
        viewonly=True)
    applied_users = db.relationship(
        'User',
        secondary='ags_users',
        primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "APPLIED")',
        viewonly=True)
    mentors = db.relationship(
        'User',
        secondary='ags_users',
        primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "MENTOR", UserAG.status == "ACTIVE")',
        viewonly=True)

    events = db.relationship('Event', secondary='ags_events')
    messages = db.relationship('Message')

    def get_hex_color(self) -> str:
        """Hex color from binary

        Takes the binary color and create valid hexadecimal color string
        including '#' (e.g. #FFFFFF for white)
        """
        return f'#{self.color.hex()}'

    def set_color(self, color: str):
        """Set binary color from hex color string
        Example: ag.set_color('#99FF23')
        
        :param color: hexadecimal color string (such as produced by 
        AG.get_hex_color). May include '#'
        :raises ValueError: color is not hex (excluding #)
        """
        self.color = bytes.fromhex(color.replace('#', ''))

    def __repr__(self):
        return f'<AG {self.name}>'


class AGSchema(Schema):
    users = Nested('UserSchema', many=True, exclude=('ags',))
    events = Nested('EventSchema', many=True, exclude=('ag',))
    association = Method('get_association', many=True)

    def get_association(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        user_ag = UserAG.query.filter_by(user_id=g.user.id,
                                         ag_id=ag_id).scalar()
        return {'role': user_ag.role, 'status': user_ag.status}

    class Meta:
        fields = (
            'id',
            'name',
            'display_name',
            'description',
            'color',
            'association',
        )


class AGSchemaIntern(Schema):
    users = Nested('UserSchema', many=True, exclude=('ags',))
    events = Nested('EventSchema', many=True, exclude=('ag',))
    actual_users = Nested('UserSchema', many=True, exclude=('ags',))
    invited_users = Nested('UserSchema', many=True, exclude=('ags',))
    applied_users = Nested('UserSchema', many=True, exclude=('ags',))
    messages = Nested('AGMessageSchema', many=True)

    read_messages = Method('get_read_messages')
    unread_messages = Method('get_unread_messages')

    def get_unread_messages(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        ag_message = db.session.query(AGMessage).join(UserAGMessage, and_(
            AGMessage.ag_id == ag_id,
            UserAGMessage.user_id == g.session.user_id,
            UserAGMessage.message_id == AGMessage.id,
            UserAGMessage.read == 0)).all()
        ag_messages_Schema = AGMessageSchema(many=True)
        return ag_messages_Schema.dump(ag_message)

    def get_read_messages(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        ag_message = db.session.query(AGMessage).join(UserAGMessage, and_(
            AGMessage.ag_id == ag_id,
            UserAGMessage.user_id == g.session.user_id,
            UserAGMessage.message_id == AGMessage.id,
            UserAGMessage.read == 1)).all()
        if len(ag_message) > 1:
            ag_messages_Schema = AGMessageSchema(many=True, exclude=('users',))
        else:
            ag_messages_Schema = AGMessageSchema(many=True, exclude=('users',))
        return ag_messages_Schema.dump(ag_message)

    class Meta:
        fields = (
            'id',
            'name',
            'display_name',
            'description',
            'users',
            'events',
            'color',
            'actual_users',
            'invited_users',
            'applied_users',
            'messages',
        )