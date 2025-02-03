from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from app import db
from app.models import User, UserProfile, FitnessGoal

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
        user.profile = UserProfile()  # Create empty profile associated with the user
        user.fitness_goal = FitnessGoal()
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


profile_model = user_ns.model('ProfileUpdate', {
    'current_weight': fields.Float(description='Current weight in kg', required=False),
    'target_weight': fields.Float(description='Target weight in kg', required=False),
    'height': fields.Float(description='Height in cm', required=False),
    'age': fields.Integer(description='Age in years', required=False),
    'body_fat_percentage': fields.Float(description='Body fat percentage', required=False),
    'muscle_mass': fields.Float(description='Muscle mass in kg', required=False)
})


@user_ns.route('/profile')
class UserProfileResource(Resource):

    @jwt_required()
    @user_ns.response(200, 'Profile retrieved successfully', profile_model)
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(404, 'Profile not found')
    def get(self):
        """Get current user's profile information"""
        current_user = User.get_current_user()

        if not current_user or not current_user.profile:
            return {"error": "Profile not found"}, 404

        return {
            "message": "Profile retrieved successfully",
            "profile": current_user.profile.to_dict()
        }, 200

    @jwt_required()
    @user_ns.expect(profile_model)
    @user_ns.response(200, "Profile updated successfully")
    @user_ns.response(400, "Invalid input data")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Profile not found")
    def put(self):
        """Update user profile information"""
        current_user = User.get_current_user()

        if not current_user or not current_user.profile:
            return {"error": "Profile not found"}, 404

        data = user_ns.payload 
        profile = UserProfile.query.filter_by(user_id=current_user.id).first()

        fields_to_update = [
            "current_weight", "target_weight", "height",
            "age", "body_fat_percentage", "muscle_mass"
        ]

        try:
            for field in fields_to_update:
                if field in data and data[field] is not None:
                    setattr(profile, field, data[field])

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

        return {
            "message": "Profile updated successfully",
            "profile": profile.to_dict()
        }, 200
