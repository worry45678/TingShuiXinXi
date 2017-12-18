import os
from pyecharts import Style
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    app配置类
    包含：SECRET_KEY;SQLALCHEMY_COMMIT_ON_TEARDOWN = True;SQLALCHEMY_TRACK_MODIFICATIONS = True;
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        初始化app配置
        """
        pass


class DevelopmentConfig(Config):
    """
    开发者配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.222.100/rx?charset=utf8'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///test2.db'


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}  # 配置名称
