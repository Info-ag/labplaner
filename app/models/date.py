"""
All Database models regarding Dates
    ---> Date
All Marshmallow Schemas regarding those models
    --> DateSchema
"""
from app.models import db


class Date(db.Model):
    """Date table

    If a specific date is needed, it will be created in this table. A 
    date is related to users (that specified their availability on that
    date) and to events (that offer this date). This way, each date will
    only occure once and it is easy to get an overview of all available
    users that signed up for that day.

    Relationships:
        - `dates_users`
        - `dates_events`
    """
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False, unique=True)

    users = db.relationship('User', secondary='dates_users')
    events = db.relationship('Event', secondary='dates_events')


class DateSchema(ma.Schema):

    class Meta:
        fields = ('id', 'day')
