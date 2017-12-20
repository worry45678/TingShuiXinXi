from . import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manger
from datetime import datetime

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

    def __repr__(self):
        return '''{"id":%d,"startdate":"%s","enddate":"%s","address":"%s","area":"%s","typename":"%s","username":"%s"}''' %(
                    self.id, self.startdate, self.enddate, self.address,self.area, self.typename.name, self.username.name)

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

    def __init__(self, **kwargs):
        super(tblUser, self).__init__(**kwargs)
        if self.role_id is None: # 如果名称为admin，则设为管理员
            if self.name == 'admin':
                self.role_id = tblRole.query.filter_by(permissions=0xff).first().id
            if self.role_id is None:
                self.role_id = tblRole.query.filter_by(default=True).first().id
    
    def can(self, permissions): # 判断角色是否包含所有请求权限，包含则返回True
        return self.role_id is not None and (self.rolename.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

class tblRole(db.Model):
    __tablename__ = 'roles'

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(16))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column('Permission', db.Integer)
    users = db.relationship('tblUser', backref='rolename', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = tblRole.query.filter_by(name=r).first()
            if role is None:
                role = tblRole(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


login_manger.anonymous_user = AnonymousUser


@login_manger.user_loader
def load_user(user_id):
    """
    加载用户，存在则返回用户对象，不存在则返回None。
    """
    return tblUser.query.get(int(user_id))