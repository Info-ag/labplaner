from app import db
import models.associations as ass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    ags = db.relationship("AG", secondary=ass.user_ag_association,
                          back_populates="users")

    def __repr__(self):
        return f"<User {self.username}>"
