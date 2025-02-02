from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ExerciseGoal, FitnessGoalsFinal, Exercises, User

fitness_goals_ns = Namespace('fitness-goals', description='Fitness Goals API')

# Exercise Goal Model
exercise_goal_model = fitness_goals_ns.model('ExerciseGoal', {
    'name': fields.String(required=True, description='Name of the exercise'),
    'current_weight': fields.Float(description='Current weight used for exercise'),
    'current_reps': fields.Integer(description='Current reps performed'),
    'target_weight': fields.Float(description='Target weight for exercise'),
    'target_reps': fields.Integer(description='Target reps for exercise')
})

# Fitness Goal Model
fitness_goal_model = fitness_goals_ns.model('FitnessGoal', {
    'id': fields.Integer(description='Fitness goal ID'),
    'current_weight': fields.Float(required=True, description='Current body weight'),
    'weight_goal': fields.Float(required=True, description='Target body weight'),
    'exercise_goals': fields.List(fields.Nested(exercise_goal_model), description='List of exercise goals')
})


@fitness_goals_ns.route('')
class FitnessGoalList(Resource):

    @fitness_goals_ns.expect(fitness_goal_model)
    @fitness_goals_ns.response(201, 'Fitness goal created successfully')
    @fitness_goals_ns.response(400, 'Invalid data provided')
    @jwt_required()
    def post(self):
        """Create a new fitness goal"""
        user, error = User.get_current_user()
        if error:
            return error
        data = request.get_json()

        if 'current_weight' not in data or 'weight_goal' not in data or 'exercise_goals' not in data:
            return {'message': 'Missing required goal information'}, 400

        exercise_goals = []
        for exercise_data in data['exercise_goals']:
            if 'name' not in exercise_data or ('current_weight' not in exercise_data and 'current_reps' not in exercise_data) or ('target_weight' not in exercise_data and 'target_reps' not in exercise_data):
                return {'message': 'Missing required exercise goal information'}, 400

            exercise = Exercises.query.filter(
                Exercises.name.ilike(exercise_data['name'])).first()
            if not exercise:
                return {'message': f'Exercise "{exercise_data["name"]}" is not available in our database'}, 400

            exercise_goal = ExerciseGoal(
                exercise_name=exercise.name,
                current_weight=exercise_data.get('current_weight'),
                current_reps=exercise_data.get('current_reps'),
                target_weight=exercise_data.get('target_weight'),
                target_reps=exercise_data.get('target_reps')
            )
            exercise_goals.append(exercise_goal)

        goal = FitnessGoalsFinal(
            user_id=user.id,
            current_weight=data['current_weight'],
            weight_goal=data['weight_goal'],
            exercise_goals=exercise_goals
        )
        db.session.add(goal)
        db.session.commit()

        return {'message': 'Fitness goal created successfully!'}, 201

    @fitness_goals_ns.response(200, 'Success', [fitness_goal_model])
    @fitness_goals_ns.response(404, 'Fitness goals not found')
    @jwt_required()
    def get(self):
        """Retrieve all fitness goals for the current user"""
        user, error = User.get_current_user()
        if error:
            return error
        goals = FitnessGoalsFinal.query.filter_by(user_id=user.id).all()

        if not goals:
            return {'message': 'Fitness goals not found'}, 404

        return {'fitness_goals': [goal.to_dict() for goal in goals]}, 200


@fitness_goals_ns.route('/<int:goal_id>')
class FitnessGoalDetail(Resource):

    @fitness_goals_ns.response(200, 'Success', fitness_goal_model)
    @fitness_goals_ns.response(404, 'Fitness goal not found')
    @jwt_required()
    def get(self, goal_id):
        """Retrieve a specific fitness goal by ID"""
        user, error = User.get_current_user()
        if error:
            return error
        goal = FitnessGoalsFinal.query.filter_by(
            id=goal_id, user_id=user.id).first()

        if not goal:
            return {'message': 'Fitness goal not found'}, 404

        return {'fitness_goal': goal.to_dict()}, 200

    @fitness_goals_ns.response(200, 'Fitness goal deleted successfully')
    @fitness_goals_ns.response(404, 'Fitness goal not found')
    @jwt_required()
    def delete(self, goal_id):
        """Delete a fitness goal by ID"""
        user, error = User.get_current_user()
        if error:
            return error
        goal = FitnessGoalsFinal.query.filter_by(
            id=goal_id, user_id=user.id).first()

        if not goal:
            return {'message': 'Fitness goal not found'}, 404

        db.session.delete(goal)
        db.session.commit()
        return {'message': 'Fitness goal deleted successfully'}, 200
