from flask_marshmallow import fields

from app import db
from app import ma


class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)

    users = db.relationship("User", secondary="user_ag_association")

    def __repr__(self):
        return f"<AG {self.name}>"


class AGSchema(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))

    class Meta:
        fields = ("id", "name", "display_name", "description", "users")
