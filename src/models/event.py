from app import db
from app import ma

from models.associations import DateEvent


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(280), nullable=False)
    date = db.Column(db.Date, nullable=True)
    ag = db.Column(db.Integer, db.ForeignKey("ags.id"))

    dates = db.relationship('Date', secondary="date_event_association")


class EventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'display_name', 'ag', 'dates')
