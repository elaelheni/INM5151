
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from economeuble.config import DevConfig
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




#Configs for the flask app

app = Flask(__name__)
app.config.from_object(DevConfig)


#Proteger les cookies
#Generated using : import secrets, secrets.token_hex()
app.config['SECRET_KEY'] = 'd13befefb81e55ad4237b37aa290777814285f80b78ad0ce6e36c08d488212fc'


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from economeuble import routes