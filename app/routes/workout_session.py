from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, SelectedExercise, User, Exercises
from app import db


workout_session_ns = Namespace(
    'workout-sessions', description='Workout Sessions')




class WorkoutSession(Resource):


    pass