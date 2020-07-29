
from datetime import datetime
from flask import Flask, render_template, make_response, redirect
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
#from forms import RegistrationForm, LoginForm


#Configs for the flask app

app = Flask(__name__)
app.config.from_object(DevConfig)

#app.config['SECRET_KEY'] = 'Shakalaka20'


db = SQLAlchemy(app)

#structure of Database

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(120), nullable=False, default='static/default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #relationship not column
    #referencing the Article class
    article = db.relationship('Article', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_profile}')"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pictures = db.Column(db.String(120), nullable=False)

    #a column, every post is related to a unique user
    #referencing the table name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.descripton}', '{self.pictures}')"


