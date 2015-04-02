from flask.ext.testing import TestCase
from flask import Flask
from SteamScout import app, db
import unittest

# Built in testing at http://flask.pocoo.org/docs/0.10/testing/
# Check out the Flask-Testing API at the very bottom of the page for more testing options
# https://pythonhosted.org/Flask-Testing/


class DatabaseAndForms(TestCase):
    
    def create_app(self):
        # Changes the app config to the testing settings before returning it.
        app.config.from_object('config.TestingConfig')        
        return app

    def setUp(self):
        db.create_all()

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

        # Settings Page
        # self.assert_404(self.client.get("/settings"))        
        
if __name__ == '__main__':
    unittest.main()