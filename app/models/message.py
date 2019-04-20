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

