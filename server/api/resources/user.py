from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from api import app, db
from api.models import User
from api.utils.security import token_required
import secrets, datetime, jwt

def check_and_get_user(public_id): 
  """ Returns object user if this user exists in DB""" 
  user = User.query.filter_by(public_id=public_id).first()
  if user: 
    return user
  else:
    return jsonify({'message': 'No user found'})

class UserIdREST(Resource):
  # Returns a specific user 
  def get(self, public_id): 
    user = check_and_get_user(public_id)
    return jsonify({'user' : user.to_dict()})

  # Update a specific user
  def put(self, public_id): 
    user = check_and_get_user(public_id)
    data = request.get_json()
    user.email = data['email']
    db.session.commit() 
    return jsonify({'message': 'The user has been updated.'})

  # Delete (desactivate) user
  def delete(self, public_id): 
    user = check_and_get_user(public_id)
    user.is_active = False
    db.session.commit() 
    return jsonify({'message': 'The user has been deleted.'})

class UserREST(Resource): 
  # Return all users
  @token_required
  def get(self, current_user): 
    users = User.query.all() 
    # Parse SQLAlchemy data to json data
    output = []
    for user in users: 
      output.append(user.to_dict())

    return jsonify({'current' : current_user.email, 'users' : output})

    # Create new user
  def post(self): 
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Add new user to database
    new_user = User(
      public_id = secrets.token_hex(6),
      email = data['email'],
      password = hashed_password, 
      username = data['username']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created'})

class LogInREST(Resource):
  def get(self):
    auth = request.authorization
    if not (auth or auth.username or auth.password): 
      return make_response(jsonify({'message' : 'Unauthorized'}), 401, {'WWW-Authenticate' : 'Basic realm="Unauthorized"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user: 
      return make_response(jsonify({'message' : 'Invalid email or password'}), 401, {'WWW-Authenticate' : 'Basic realm="Invalid email or password"'})
    
    if check_password_hash(user.password, auth.password):
      # User found: we generate a Json Web Token (JWT)
      token = jwt.encode({
        'public_id': user.public_id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
      return jsonify({'token' :  token.decode('UTF-8')})
    else: 
      return make_response(jsonify({'message' : 'Invalid email or password'}), 401, {'WWW-Authenticate' : 'Basic realm="Invalid email or password"'})