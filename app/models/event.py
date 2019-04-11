'''
All Database models regarding events
    --> Event
All Marshmallow Schemas regarding those models
    --> EventSchema
'''

from marshmallow import Schema, Nested

from app.models import db

from app.models.ag import AGSchema


class Event(db.Model):
    """Events are used to plan meetings

    One event can only happen on one day (Event.date). Using the
    `events_dates` relationship, we can specify possible dates on which
    the event can take place. Each event is bound to at least one 
    working group (AG) using the `ags_events` table.

    Relationships:
        - `events_dates`
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    display_name = db.Column(db.String(length=48), nullable=False)
    description = db.Column(db.Text(length=280), nullable=True)
    date = db.Column(db.Date, nullable=True)
    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))

    ag = db.relationship('AG')
    dates = db.relationship('Date', secondary='dates_events')
    ags = db.relationship('Date', secondary='ags_events')


class EventSchema(Schema):
    ag = Nested(AGSchema)
    dates = Nested('DateSchema', many=True)

    class Meta:
        fields = ('id', 'date', 'display_name', 'ag', 'dates')
