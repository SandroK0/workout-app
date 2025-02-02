from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import WorkoutPlanFinal, Exercises, User
import json

workout_plans_ns = Namespace('workout-plans', description='Workout Plans')

# Exercise Model (Used inside WorkoutPlan)
exercise_model = workout_plans_ns.model('Exercise', {
    'name': fields.String(required=True, description='Name of the exercise'),
    'difficulty': fields.String(description='Difficulty level'),
    'target_muscles': fields.String(description='Targeted muscle groups'),
    'instructions': fields.String(description='Exercise instructions'),
    'sets': fields.Integer(description='Number of sets'),
    'reps': fields.Integer(description='Number of reps per set'),
    'duration': fields.String(description='Duration of the exercise (if applicable)'),
    'distance': fields.String(description='Distance (if applicable)')
})

#  Workout Plan Model (For Request & Response)
workout_plan_model = workout_plans_ns.model('WorkoutPlan', {
    'id': fields.Integer(description='Workout Plan ID'),
    'name': fields.String(required=True, description='Name of the workout plan'),
    'frequency': fields.String(required=True, description='Workout frequency (e.g., 3x per week)'),
    'goal': fields.String(required=True, description='Fitness goal'),
    'session_duration': fields.String(required=True, description='Duration per session'),
    'selected_exercises': fields.List(fields.Nested(exercise_model), description='List of selected exercises')
})

# Request Model for Creating Workout Plan
workout_plan_request_model = workout_plans_ns.model('WorkoutPlanRequest', {
    'workout_name': fields.String(required=True, description='Name of the workout plan'),
    'frequency': fields.String(required=True, description='Workout frequency'),
    'goal': fields.String(required=True, description='Fitness goal'),
    'session_duration': fields.String(required=True, description='Duration per session'),
    'selected_exercises': fields.List(fields.Nested(exercise_model), required=True, description='List of exercises')
})

# Response Model for Success & Errors
message_model = workout_plans_ns.model('MessageResponse', {
    'message': fields.String(description='Response message')
})


@workout_plans_ns.route('')
class WorkoutPlanList(Resource):

    @workout_plans_ns.expect(workout_plan_request_model)
    @workout_plans_ns.response(201, 'Workout plan created successfully', message_model)
    @workout_plans_ns.response(400, 'Invalid data provided', message_model)
    @jwt_required()
    def post(self):
        """Create a new workout plan"""

        user, error = User.get_current_user()
        if error:
            return error

        data = request.get_json()

        required_fields = ['workout_name', 'frequency',
                           'goal', 'session_duration', 'selected_exercises']
        if not all(field in data for field in required_fields):
            return {'message': 'Invalid data provided'}, 400

        selected_exercises = []
        for exercise_data in data['selected_exercises']:
            name = exercise_data['name'].strip()
            exercise = Exercises.query.filter(
                Exercises.name.ilike(name)).first()
            if not exercise:
                return {'message': f'Exercise "{name}" is not available in our database'}, 400

            selected_exercises.append({
                'name': exercise.name,
                'difficulty': exercise.difficulty,
                'target_muscles': exercise.target_muscles,
                'instructions': exercise.instructions,
                'sets': exercise_data.get('sets'),
                'reps': exercise_data.get('reps'),
                'duration': exercise_data.get('duration'),
                'distance': exercise_data.get('distance')
            })

        new_workout_plan = WorkoutPlanFinal(
            user_id=user.id,
            name=data['workout_name'],
            frequency=data['frequency'],
            goal=data['goal'],
            session_duration=data['session_duration'],
            selected_exercises=json.dumps(selected_exercises)
        )

        db.session.add(new_workout_plan)
        db.session.commit()

        return {'message': 'Workout plan created successfully'}, 201

    @workout_plans_ns.response(200, 'Success', [workout_plan_model])
    @workout_plans_ns.response(404, 'Workout plans not found', message_model)
    @jwt_required()
    def get(self):
        """Retrieve all workout plans for the current user"""
        user, error = User.get_current_user()
        if error:
            return error

        workout_plans = WorkoutPlanFinal.query.filter_by(user_id=user.id).all()

        if not workout_plans:
            return {'message': 'Workout plans not found'}, 404

        response_data = [{
            'id': plan.id,
            'name': plan.name,
            'frequency': plan.frequency,
            'goal': plan.goal,
            'session_duration': plan.session_duration,
            'selected_exercises': json.loads(plan.selected_exercises)
        } for plan in workout_plans]

        return {'workout_plans': response_data}, 200


@workout_plans_ns.route('/<int:workout_id>')
class WorkoutPlanDetail(Resource):

    @workout_plans_ns.response(200, 'Success', workout_plan_model)
    @workout_plans_ns.response(404, 'Workout plan not found', message_model)
    @jwt_required()
    def get(self, workout_id):
        """Retrieve a specific workout plan by ID"""
        user, error = User.get_current_user()
        if error:
            return error
        workout_plan = WorkoutPlanFinal.query.filter_by(
            id=workout_id, user_id=user.id).first()

        if not workout_plan:
            return {'message': 'Workout plan not found'}, 404

        plan_data = {
            'id': workout_plan.id,
            'name': workout_plan.name,
            'frequency': workout_plan.frequency,
            'goal': workout_plan.goal,
            'session_duration': workout_plan.session_duration,
            'selected_exercises': json.loads(workout_plan.selected_exercises)
        }

        return {'workout_plan': plan_data}, 200


@workout_plans_ns.route('/<int:workout_plan_id>')
class WorkoutPlanDelete(Resource):

    @workout_plans_ns.response(200, 'Workout plan deleted successfully', message_model)
    @workout_plans_ns.response(404, 'Workout plan not found', message_model)
    @jwt_required()
    def delete(self, workout_plan_id):
        """Delete a workout plan by ID"""
        user, error = User.get_current_user()
        if error:
            return error

        workout_plan = WorkoutPlanFinal.query.filter_by(
            id=workout_plan_id, user_id=user.id).first()

        if not workout_plan:
            return {'message': 'Workout plan not found'}, 404

        db.session.delete(workout_plan)
        db.session.commit()
        return {'message': 'Workout plan deleted successfully'}, 200
