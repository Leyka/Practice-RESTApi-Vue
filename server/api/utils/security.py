from flask import request, jsonify
from functools import wraps
from api import app
from api.models import User
import jwt


def token_required(func):
  """ Decorator
  For each action, check if it's the good user that is doing the request
  by checking the token (JWT) in the headers of the request.
  """
  @wraps(func)
  def decorated(*args, **kwargs): 
    token = None
 
    # Check if tehre is a token?
    if 'x-access-token' in request.headers: 
      token = request.headers['x-access-token']
    else: 
      return jsonify({'message' : 'Token is missing'}), 401
    # Now check if it's the good token
    try: 
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(public_id=data['public-id']).first()
    except: 
      return jsonify({'message' : 'Token is invalid'}), 401
    # Everything is good, pass the current user to the route 
    return func(current_user, *args, **kwargs)

  return decorated