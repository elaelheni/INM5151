from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from .database import Database
import re


app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404