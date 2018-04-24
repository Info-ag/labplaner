from app import db
import models.associations as ass


class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(250), unique=True, nullable=False)

    users = db.relationship("User", secondary=ass.user_ag_association,
                            back_populates="ags")

    def __repr__(self):
        return f"<AG {self.name}>"
