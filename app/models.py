from . import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manger

class tblData(db.Model):  # 停水数据表model
    __tablename__ = "tblData"  # 表名

    # 表结构,具体更多的数据类型自行百度
    id = db.Column("ID", db.Integer, primary_key=True, autoincrement=True)
    startdate = db.Column("StartDate", db.DateTime)
    enddate = db.Column("EndDate", db.DateTime, nullable=True)
    address = db.Column("Address", db.Text)
    area = db.Column("Area", db.Text)
    type_id = db.Column("typeid", db.ForeignKey('tblType.ID'))
    user_id = db.Column("userid", db.ForeignKey('tblUser.ID'))

class tblType(db.Model):
    __tablename__ = "tblType"

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(10), unique=True, index=True)
    datas = db.relationship('tblData', backref='typename')

class tblUser(UserMixin, db.Model):
    __tablename__ = "tblUser"

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(8))
    password_hash = db.Column('password', db.String(128))
    datas = db.relationship('tblData', backref='username')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.ID'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)

class tblRole(db.Model):
    __tablename__ = 'roles'

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(10))
    premission = db.Column('Premission', db.String(10))
    users = db.relationship('tblUser', backref='rolename')

@login_manger.user_loader
def load_user(user_id):
    """
    加载用户，存在则返回用户对象，不存在则返回None。
    """
    return tblUser.query.get(int(user_id))