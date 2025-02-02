from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from app.models import Exercises, User
from flask import request
import logging

exercises_ns = Namespace('exercises', description='Exercises')

# Model for response documentation (Optional)
exercise_model = exercises_ns.model('Exercise', {
    'exercise_id': fields.Integer(required=True, description='The unique identifier of the exercise'),
    'name': fields.String(required=True, description='The name of the exercise'),
    'description': fields.String(required=True, description='A description of the exercise'),
    'created_at': fields.String(required=True, description='Creation timestamp of the exercise'),
    'updated_at': fields.String(required=True, description='Last updated timestamp of the exercise')
})


@exercises_ns.route("")
class GetExercises(Resource):
    @exercises_ns.response(200, 'Success', [exercise_model])
    @exercises_ns.response(401, 'Unauthorized')
    @exercises_ns.doc(security='BearerAuth') 
    @jwt_required()
    def get(self):
        user, error = User.get_current_user()
        if error:
            return error
        exercises = Exercises.query.all()
        return {'exercises': [exercise.to_dict() for exercise in exercises]}


@exercises_ns.route("/<int:exercise_id>")
class GetExercise(Resource):
    @exercises_ns.response(200, 'Success', exercise_model)
    @exercises_ns.response(401, 'Unauthorized')
    @exercises_ns.response(404, 'Exercise Not Found')
    @exercises_ns.doc(security='BearerAuth') 
    @jwt_required()
    def get(self, exercise_id):
        exercise = Exercises.query.filter_by(exercise_id=exercise_id).first()
        if exercise:
            return {'exercise': exercise.to_dict()}
        else:
            return {'message': 'Exercise not found'}, 404
