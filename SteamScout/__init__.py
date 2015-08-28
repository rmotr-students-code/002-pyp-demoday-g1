"""Initializes SteamScout with SQLAlchemy, Bcrypt, Bootstrap, Flask-Mail and LoginManager"""
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from flask.ext.mail import Mail
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)

app.config.from_object('config.LocalConfig')

# SQLAlchemy Initialization
db = SQLAlchemy(app)

# Bootstrap Initialization
Bootstrap(app)

# Bcrypt Initialization
flask_bcrypt = Bcrypt(app)

# Mail Initialization
mail = Mail()
mail.init_app(app)

# Login Manager Initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from SteamScout.views import *

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
