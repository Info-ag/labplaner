"""
copied from AGMessage:
    class AGMessage(db.Model):
        __tablename__ = 'ag_messages'
        id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
        ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))
        subject = db.Column(db.String(20))
        message = db.Column(db.String(1000))
        created = db.Column(db.DateTime, default=datetime.now())

        users = db.relationship('UserAGMessage', secondary='users', \
                                primaryjoin='and_(AGMessage.id == UserAGMessage.message_id, UserAGMessage.user_id == User.id)',
                                viewonly=True)

        def __repr__(self):
            return f'<AGMessage {self.id}>'

    class AGMessageSchema(Schema):
        read = Method('get_read_status')
        users = Nested('UserAGMessageSchema', many=True)

        def get_read_status(self, obj: AGMessage):
            if not g.session.authenticated:
                return None
            user_ag_message = db.session.query(UserAGMessage).filter_by(
                user_id=g.session.user_id, message_id=obj.id).scalar()
            return user_ag_message.read

        class Meta:
            fields = (
                'id',
                'ag_id',
                'subject',
                'message',
                'read',
                'created',
                'users',
            )


    class Message(db.Model):
        __tablename__ = 'messages'
        id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
        subject = db.Column(db.String(20))
        message = db.Column(db.String(1000))
        created = db.Column(db.DateTime, default=datetime.now())

        def __repr__(self):
            return f'<Message {self.id}>'

"""

from datetime import datetime

from app.models import db


__all__ = ['Message']


class Message(db.Model):
    """Message

    Messages only have an author. They are either connected to a working
    group (AG) or to an individual user (recepient).

    :param id:
    :param message:
    :param time:
    :param author_id:
    :param ag_id:
    :param recepient_id:

    Relationships:
        - users_messages: status of a message (recepient only)
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    message = db.Column(db.Text(1000), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'), nullable=True)
    recepient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    author = db.relationship(
        'User',
        back_populates='messages',
        primaryjoin='User.id == Message.author_id',)
    recepient = db.relationship(
        'User',
        back_populates='messages',
        primaryjoin='User.id == Message.recepient_id',)
    ag = db.relationship('AG', back_populates='messages')

