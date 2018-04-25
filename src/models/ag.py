from app import db
from app import ma
import models.associations as ass


class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)

    users = db.relationship("User", secondary=ass.user_ag_association,
                            back_populates="ags")

    def __repr__(self):
        return f"<AG {self.name}>"


class AGSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "display_name", "description")