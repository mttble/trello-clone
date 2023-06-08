from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import  create_access_token
from datetime import timedelta
from models.user import User, UserSchema
from init import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Parse, sanitise and validate the incoming JSON data
        # via the schema.
        user_info = UserSchema().load(request.json)
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
            name=user_info['name'],
        )
        
        # Add and commit the new user
        db.session.add(user)
        db.session.commit()

        # Return new user information
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409
    
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).where(User.email==request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(hours=4))
            return {'token':token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400