from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from app import db
from app.models import User

user_ns = Namespace('user', description='User')

user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The username'),
})

register_model = user_ns.model('Register', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password'),
})

login_model = user_ns.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password'),
})


def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return None, 404
    return user, 200


@user_ns.route('/register')
class Register(Resource):
    @user_ns.expect(register_model)
    @user_ns.response(201, 'User registered successfully')
    @user_ns.response(400, 'Missing required fields')
    @user_ns.response(409, 'Username already taken')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Missing required fields", "message": "Username and password are required to register."}, 400

        if len(password) < 8:
            return {"error": "Weak password", "message": "Password must be at least 8 characters long."}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "Conflict", "message": "The username is already taken."}, 409

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {
            "message": "User registration successful",
            "user": {"id": user.id, "username": user.username}
        }, 201


@user_ns.route('/login')
class Login(Resource):
    @user_ns.expect(login_model)
    @user_ns.response(200, 'Login successful')
    @user_ns.response(400, 'Missing required fields')
    @user_ns.response(401, 'Invalid credentials')
    def post(self):
        """Login a user"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Missing required fields", "message": "Both username and password are required."}, 400

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"error": "Invalid credentials", "message": "Invalid username or password."}, 401

        access_token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=1))

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {"id": user.id, "username": user.username}
        }, 200
