from flask import Flask, request, render_template, redirect, session, json, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.openid import OpenID

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    #app.config['SQLALCHEMY_DATABASE_URI'] = #
    Bootstrap(app)
    db = SQLAlchemy(app)
    oid = OpenID(app)
    
    
    #routes
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/games')
    def games():
        # page that shows all the games.
        return render_template('games.html')

    @app.route('/developers')
    def show_developors():
        # page that shows all the games.
        return render_template('developers.html')

    @app.route('/contact')
    def contact():
        # page that shows all the games.
        return render_template('contact.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')
        
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')        
    
    @app.route('/settings')
    def settings():
        pass
    
    return app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=8080, debug=True) # We have to remember to change debug = True back to False if we deply to heruku
