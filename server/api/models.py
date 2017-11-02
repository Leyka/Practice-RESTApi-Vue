from api import db
from datetime import datetime

class User(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(50))
  username = db.Column(db.String(20), unique=True)
  created_at = db.Column(db.DateTime, default=datetime.now)
  is_active = db.Column(db.Boolean, default=True)

  def to_dict(self):
    """ Cast User object to dictionnary """  
    return {
        'public_id': self.public_id, 
        'email': self.email, 
        'password': self.password, 
        'username': self.username, 
        'created_at': self.created_at,
        'is_active': self.is_active
    }

class Post(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text)
  user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)