from app import db

user_ag_association = db.Table('user_ag_association', db.Model.metadata,
                               db.Column('uid', db.Integer, db.ForeignKey('users.id')),
                               db.Column('ag_id', db.Integer, db.ForeignKey('ags.id')),
                               db.Column('role', db.String(11), nullable=False, default="NONE")
                               #normal roles: 'PARTICIPANT' and 'MENTOR', 'NONE' as default value
                               )
