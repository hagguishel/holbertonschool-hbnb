import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://<user>:<password>@localhost/<db_name>"

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
