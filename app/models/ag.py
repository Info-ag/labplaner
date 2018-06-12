from app import db, ma
from sqlalchemy import and_
from app.models.associations import UserAG 
from flask import g

class AG(db.Model):
    __tablename__ = 'ags'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    color = db.Column(db.String())
    # enum: primary, success, dark, warning, error
    display_name = db.Column(db.String(48), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)

    users = db.relationship('User', secondary='users_ags', order_by='UserAG.role')

    actual_users = db.relationship('User', secondary='users_ags', primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role != "NONE")', viewonly=True)
    invited_users = db.relationship('User', secondary='users_ags', primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "INVITED")', viewonly=True)
    applied_users = db.relationship('User', secondary='users_ags', primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "NONE", UserAG.status == "APPLIED")', viewonly=True)
    mentors = db.relationship('User', secondary='users_ags', primaryjoin='and_(User.id == UserAG.user_id, AG.id == UserAG.ag_id, UserAG.role == "MENTOR", UserAG.status == "ACTIVE")', viewonly=True)
    events = db.relationship('Event')

    def __repr__(self):
        return f'<AG {self.name}>'


class AGSchema(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))
    association = ma.Method('get_association', many=True)
    def get_association(self, obj: AG):
        if not g.session.authenticated:
            return None
        ag_id = obj.id
        user_ag = UserAG.query.filter_by(user_id=g.user.id, ag_id=ag_id).scalar()
        return {'role': user_ag.role, 'status': user_ag.status}

    class Meta:
        fields = ('id', 'name', 'display_name', 'description', 'color', 'association')


class AGSchemaIntern(ma.Schema):
    users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    events = ma.Nested('EventSchema', many=True, exclude=('ag',))
    actual_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    invited_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    applied_users = ma.Nested('UserSchema', many=True, exclude=('ags',))
    class Meta:
        fields = ('id', 'name', 'display_name', 'description', 'users', 'events', 'color', 'actual_users', 'invited_users', 'applied_users')
