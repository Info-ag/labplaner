from app import db
from app import ma

from models.event import Event

from models.associations import DateUser, DateEvent

class Date(db.Model):
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False)

    events = db.relationship('Event', secondary="date_event_association")
    users = db.relationship('User', secondary="user_date_asscociation")


class LockedDates(db.Model):
    __tablename__ = 'lockeddates'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False)
    users = db.relationship('User', secondary="user_date_asscociation")


class DateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'day', 'events')
