from app import db


class UserAG(db.Model):
    __tablename__ = 'user_ag_association'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    agid = db.Column(db.Integer, db.ForeignKey('ags.id'))
    role = db.Column('role', db.String(11), nullable=False, default="NONE")

    def __repr__(self):
        return f"<UserAG {self.role}>"


class DateEvent(db.Model):
    __tablename__ = 'date_event_association'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    dtid = db.Column(db.Integer, db.ForeignKey('dates.id'))
    evid = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"<DateEvent {self.role}>"


class DateUser(db.Model):
    __tablename__ = 'user_date_asscociation'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    dtid = db.Column(db.Integer, db.ForeignKey('dates.id'))
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<DateUser {self.role}>"
