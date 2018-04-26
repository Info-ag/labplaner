from app import db
from app import ma

class Date(db.Model)
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False)

    dates = db.relationship('Event', secondary="date_event_association")
