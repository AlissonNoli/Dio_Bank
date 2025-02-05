import os

class Config():
    TESTING = False
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SECRET_KEY=os.getenv('dev'),
    SQLALCHEMY_DATABASE_URI=os.getenv('sqlite:///blog.sqlite'),
    JWT_SECRET_KEY=os.getenv('super-secret-key')

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY= "test",
    DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = "test" 