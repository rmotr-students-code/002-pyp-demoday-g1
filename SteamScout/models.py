from app import db, oid
from flask import g, session

#A model which will store the users steam ID for Sign in
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(40))
    nickname = db.String(80)
    
    def __init__(self, steam_id, nickname):
        self.steam_id = steam_id
        self.nickname = nickname
    
    def __repr__(self):
        return '<nickname: {}>'.format(self.nickname)

#Add user to db if he does not exist in db    
""""@staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first() # not quite sure what the issue is here
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db.session.add(rv)
        return rv
        """