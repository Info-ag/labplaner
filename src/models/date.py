from app import db
from app import ma


class Date(db.Model):
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False)

    event = db.Column(db.Integer, db.ForeignKey('events.id'))

    events = db.relationship('Event', secondary="events_dates")
    users = db.relationship('User', secondary="users_dates")


class DateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'day', 'event', 'events')
