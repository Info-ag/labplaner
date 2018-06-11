from app import db


class UserAG(db.Model):
    __tablename__ = 'users_ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ag_id = db.Column(db.Integer, db.ForeignKey('ags.id'))
    role = db.Column(db.String(11), nullable=False, default='NONE')
    status = db.Column(db.String(11), nullable=False, default='NONE')

    # either 'MENTOR', 'PARTICIPANT' or 'NONE'

    def __repr__(self):
        return f'<UserAG {self.id}>'


class EventDate(db.Model):
    __tablename__ = 'events_dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    date_id = db.Column(db.Integer, db.ForeignKey('dates.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f'<EventDate {self.id}>'


class UserDate(db.Model):
    __tablename__ = 'users_dates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    date_id = db.Column(db.Integer, db.ForeignKey('dates.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f'<UserDate {self.id}>'
