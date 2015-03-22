from flask.ext.login import UserMixin
from SteamScout import app, db 
# UserMixin contains the properties andmethods required by flask-login 
# for our user object
class User(db.Model, UserMixin): 
    __tablename__= 'user'
    #changed user_id to id

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)  
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(10))
    registered_on = db.Column(db.DateTime)

    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self):
        return '<ID: {} name: {}>'.format(self.id,self.username)
    
    #Methods included by UserMixin:
    """
    is_authenticated, is_active, is_anonymous, get_id
    """
    

class Preferences(db.Model): 
    __tablename__= 'preferences'
    preference_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    game_id=db.Column(db.Integer)
    game_name = db.Column(db.String, unique=True)
    threshold_amount=db.Column(db.Float)
    
    def __init__(self, user_id, game_id, game_name, threshold_amount): 
        self.user_id = user_id
        self.game_id = game_id
        self.game_name = game_name
        self.threshold_amount = threshold_amount
        
    def __repr__(self):
        return 'UserID: {} -- Game: {} -- Threshold: {}>'.format(self.user_id,
                                        self.game_name, self.threshold_amount)

class Games(db.Model):
    __tablename__='games'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, unique=True)
    game_name = db.Column(db.String, unique=True)
    
    def __init__(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name
 
    def __repr__(self):
        return 'Game:{} -- Game ID{}'.format(self.game_name, self.game_id)
 
### Uncomment to create DB ####        
#db.create_all()