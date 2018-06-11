from app import db, ma

from app.models.event import EventSchema


class Date(db.Model):
    __tablename__ = 'dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Date, nullable=False, unique=True)

    users = db.relationship('User', secondary='users_dates')
    events = db.relationship('Event', secondary='events_dates')


class DateSchema(ma.Schema):
    count = ma.Method('count_users')

    def count_users(self, obj: Date):
        event_id = self.context.get('event_id')
        users = []
        for user in obj.users:  # that
            for ag in user.ags:  # shit
                for event in ag.events:  # is
                    if event.id == event_id:  # damn
                        users.append(user)  # nested

        return len(users)

    class Meta:
        fields = ('id', 'day', 'count')
