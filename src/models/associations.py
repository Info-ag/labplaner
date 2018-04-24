from app import db

user_ag_association = db.Table('user_ag_association', db.Model.metadata,
                               db.Column('uid', db.Integer, db.ForeignKey('users.id')),
                               db.Column('ag_id', db.Integer, db.ForeignKey('ags.id'))
                               )
