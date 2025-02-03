from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, SelectedExercise, User, Exercises
from app import db


workout_plans_ns = Namespace('workout-plans-exercize', description='Workout Plans Exercises')
