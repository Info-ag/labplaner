from app import db
from app import ma

from models.event import EventSchema


class Date(db.Model):
    __tablename__ = 'dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    ag = db.Column(db.Integer, db.ForeignKey('ags.id'))

    users = db.relationship('User', secondary="users_dates")


class DateSchema(ma.Schema):
    event = ma.Nested(EventSchema, exclude=('dates',))

    class Meta:
        fields = ('id', 'day', 'event')
