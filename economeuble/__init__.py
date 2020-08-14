
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from economeuble.config import DevConfig
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




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

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'economeuble.recup@gmail.com'
app.config['MAIL_PASSWORD'] = 'Shakalaka20'

mail = Mail(app)

from economeuble import routes