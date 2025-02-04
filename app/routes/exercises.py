from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models import Exercises, User

exercises_ns = Namespace('exercises', description='Exercises')

exercise_model = exercises_ns.model('Exercise', {
    'id': fields.Integer(required=True, description='The unique identifier of the exercise'),
    'name': fields.String(required=True, description='The name of the exercise'),
    'description': fields.String(required=True, description='A description of the exercise'),
    'instructions': fields.String(required=True, description='Instructions for the exercise'),
    'target_muscles': fields.String(required=True, description='Target muscles'),
    'difficulty': fields.Integer(required=True, description='Difficulty of the exercise')
})


@exercises_ns.route("")
class ExercisesList(Resource):
    @exercises_ns.response(200, 'Success', [exercise_model])
    @exercises_ns.response(404, 'Exercises Not Found')
    def get(self):
        exercises = Exercises.query.all()

        if not exercises:
            return {'message': 'Exercises not found'}, 404

        return {'exercises': [exercise.to_dict() for exercise in exercises]}, 200


@exercises_ns.route("/<int:exercise_id>")
class Exercise(Resource):
    @exercises_ns.response(200, 'Success', exercise_model)
    @exercises_ns.response(404, 'Exercise Not Found')
    def get(self, exercise_id):
        exercise = Exercises.query.filter_by(id=exercise_id).first()
        if exercise:
            return {'exercise': exercise.to_dict()}, 200
        else:
            return {'message': 'Exercise not found'}, 404
