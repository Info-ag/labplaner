from app import db


class UserAG(db.Model):
    __tablename__ = 'user_ag_association'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    agid = db.Column(db.Integer, db.ForeignKey('ags.id'))
    role = db.Column('role', db.String(11), nullable=False, default="NONE")

    def __repr__(self):
        return f"<UserAG {self.role}>"
