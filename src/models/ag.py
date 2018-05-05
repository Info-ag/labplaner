from app import db
from app import ma


class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    color = db.Column(db.String())
    # enum: primary, success, dark, warning, error
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)

    users = db.relationship("User", secondary="users_ags")
    events = db.relationship("Event")

    def __repr__(self):
        return f"<AG {self.name}>"


class AGSchema(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))

    class Meta:
        fields = ("id", "name", "display_name", "description", "color")


class AGSchemaIntern(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))

    class Meta:
        fields = ("id", "name", "display_name", "description", "users", "events", "color")
