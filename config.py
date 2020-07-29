
#Configurations pour la Flask app

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False