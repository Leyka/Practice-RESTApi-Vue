import os, binascii
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/reflets.db'

db = SQLAlchemy(app)

# Import and register blueprint
from api.resources.user import UserREST, UserIdREST, LogInREST
api.add_resource(UserREST, '/user')
api.add_resource(UserIdREST, '/user/<public_id>')
api.add_resource(LogInREST, '/login')

app.register_blueprint(api_bp)