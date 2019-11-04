# -*- coding:utf-8 -*-

from app import db, app
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


user_role = db.Table('user_role',db.Column('user_id', db.Integer, db.ForeignKey('user.id')),db.Column('role_id', db.Integer, db.ForeignKey('role.id')))




class User(db.Model):
    __tablename__ =  'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    name = db.Column(db.String(255))    
    password = db.Column(db.String(128))
    email = db.Column(db.String(255))
    sex = db.Column(db.Integer)
    addr = db.Column(db.String(255))                                                                                                                   
    avatar = db.Column(db.TEXT)
    roles = db.relationship('Role', secondary=user_role, back_populates='users')

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration = 6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        roles=[i.name for i in self.roles]
        return s.dumps({'id':self.id,'username':self.username,'roles':roles})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    comment = db.Column(db.TEXT)
    users = db.relationship('User', secondary=user_role, back_populates='roles') 
    def __repr__(self):
        return 'Role:%s'% self.name
