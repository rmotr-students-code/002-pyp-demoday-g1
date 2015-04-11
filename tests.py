from flask.ext.testing import TestCase
from SteamScout import app, db
from SteamScout.models import User, Games, Preferences
from admin import reset_game_db
import unittest
import os


class DatabaseAndForms(TestCase):
    _basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'test_db.sqlite')
    TESTING = True

    def create_app(self):
        # Changes the app config to the testing settings before returning it.
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def test_add_user(self):

        users = User.query.filter_by(username='test_user').count()
        self.assertEqual(users, 0)
        user = User('test_user', 'example@sample.com', 'password')
        db.session.add(user)
        db.session.commit()
        users = User.query.filter_by(username='test_user').count()
        self.assertEqual(users, 1)

    def test_add_games(self):

        games_count = Games.query.count()
        assert games_count == 0

        reset_game_db()
        games_count = Games.query.count()
        assert games_count >= 1

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

class Templates(TestCase):
    
    def create_app(self):
        # Changes the app config to the testing settings before returning it.
        app.config.from_object('config.TestingConfig')
        return app
        
    render_templates = False
    
    def test_templates_renders(self):
        
        # Home Page
        response = self.client.get("/")
        self.assert_template_used('home.html')
        
        # Games Page
        response = self.client.get("/games")
        self.assert_template_used('games.html')
        
        # Developers Page
        response = self.client.get("/developers")
        self.assert_template_used('developers.html')
        
        # Contact Page
        response = self.client.get("/contact")
        self.assert_template_used('contact.html')

        
if __name__ == '__main__':
    unittest.main()