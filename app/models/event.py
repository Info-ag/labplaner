from app import db, ma

from app.models.ag import AGSchema


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    display_name = db.Column(db.String(48), nullable=False)
    description = db.Column(db.String(280), nullable=False)
    date = db.Column(db.Date, nullable=True)
    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))

    ag = db.relationship('AG')
    dates = db.relationship('Date', secondary='events_dates')


class EventSchema(ma.Schema):
    ag = ma.Nested(AGSchema)
    dates = ma.Nested('DateSchema', many=True)

    class Meta:
        fields = ('id', 'date', 'display_name', 'ag', 'dates')
