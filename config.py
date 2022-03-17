import os
class Config:
    '''
    General configuration parent class
    '''
  


    SECRET_KEY = os.environ["SECRET_KEY"]
    # UPLOADED_PHOTOS_DEST ='app/static/photos
    
    
    #email configuration[]
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ("MAIL_PASSWORD")

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
   

    SQLALCHEMY_DATABASE_URI = os.environ("DATABASE_URL")
    # if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            
    #     SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://",1)


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:2020@localhost/services'
    DEBUG = True
    
config_options = {
'development':DevConfig,
'production':ProdConfig
}