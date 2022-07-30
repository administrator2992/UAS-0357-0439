from flask_sqlalchemy import SQLAlchemy
import bcrypt
import secrets
import datetime
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class News(db.Model):
    __tablename__ = 'news'
    
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500))
    content = db.Column(db.String(500))
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())
    flag = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return

class User(db.Model):
    __tablename__ = 'users'
    
    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    uname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    read_key = db.Column(db.String(100), nullable=False, default=secrets.token_urlsafe(16))
    write_key = db.Column(db.String(100), nullable=False, default=secrets.token_urlsafe(16))
    relasi = db.relationship('News', primaryjoin="or_(User.users_id==News.created_by, User.users_id==News.updated_by)", lazy='dynamic')

    @classmethod
    def get_or_404_via_username(cls, params):
        one = User.query.filter_by(uname=params).first()
        # print(one)
        if not one:
            return None
        return one

    @classmethod
    def getname_byreadkey(cls, params):
        one = User.query.filter_by(read_key=params).first()
        schema = UserSchema()
        data = schema.dump(one)
        # print(one)
        if data['uname'] != 'admin87':
            return None
        return True

    @classmethod
    def getname_bywritekey(cls, params):
        one = User.query.filter_by(write_key=params).first()
        schema = UserSchema()
        data = schema.dump(one)
        # print(one)
        if data['uname'] != 'admin87':
            return None
        return True

    @classmethod
    def get_idwrite(cls, params):
        one = User.query.filter_by(write_key=params).first()
        schema = UserSchema()
        data = schema.dump(one)
        return data['users_id']

    def save(self):
        db.session.add(self)
        db.session.commit()
        return

    def hash_password(self, password):
        password = bcrypt.hashpw(password.encode(
            "utf-8"), bcrypt.gensalt())
        self.password = password.decode("utf-8")
        return True

    def verify_password(self, password):
        result = bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        return result

    @classmethod
    def verify_apiRead(cls, params):
        one = User.query.filter_by(read_key=params).first()
        schema = UserSchema()
        data = schema.dump(one)
        if data['read_key'] == params:
            return True
        else:
            return False
    
    @classmethod
    def verify_apiWrite(cls, params):
        one = User.query.filter_by(write_key=params).first()
        schema = UserSchema()
        data = schema.dump(one)
        if data['write_key'] == params:
            return True
        else:
            return False

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    users_id = ma.auto_field()
    name = ma.auto_field()
    uname = ma.auto_field()
    read_key = ma.auto_field()
    write_key = ma.auto_field()

class NewsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = News

    news_id = ma.auto_field()
    title = ma.auto_field()
    content = ma.auto_field()
    datetime = ma.auto_field()
    flag = ma.auto_field()
    created_by = ma.auto_field()
    updated_by = ma.auto_field()