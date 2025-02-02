from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, SelectedExercise, WorkoutGoal, ExerciseGoal, User, Exercises
from sqlalchemy.exc import SQLAlchemyError
from app import db


workout_ns = Namespace('workout_plans', description='Workout Plans Operations')

# Model for exercise goals
exercise_goal_model = workout_ns.model('ExerciseGoal', {
    'target_sets': fields.Integer(required=True),
    'target_reps': fields.Integer(required=True),
    'target_duration': fields.String,
    'target_distance': fields.String
})

# Model for selected exercises
selected_exercise_model = workout_ns.model('SelectedExercise', {
    'exercise_id': fields.Integer(required=True),
    'sets': fields.Integer,
    'reps': fields.Integer,
    'duration': fields.String,
    'distance': fields.String,
    'goals': fields.List(fields.Nested(exercise_goal_model))
})

# Model for workout goal
workout_goal_model = workout_ns.model('WorkoutGoal', {
    'target_weight': fields.Float(required=True)
})

# Main workout plan model
workout_plan_model = workout_ns.model('WorkoutPlan', {
    'name': fields.String(required=True),
    'frequency': fields.String,
    'session_duration': fields.Integer,
    'selected_exercises': fields.List(fields.Nested(selected_exercise_model), required=True),
    'workout_goal': fields.Nested(workout_goal_model, required=True)
})

# Response model
workout_plan_response = workout_ns.model('WorkoutPlanResponse', {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'frequency': fields.String,
    'session_duration': fields.Integer,
    'created_at': fields.DateTime,
    'selected_exercises': fields.List(fields.Nested(selected_exercise_model)),
    'workout_goal': fields.Nested(workout_goal_model)
})


'''
    Example request body for creating workout plan.

    {
    "name": "Beginner Full Body Routine",
    "frequency": "3 times/week",
    "session_duration": 60,
    "selected_exercises": [
        {
        "exercise_id": 1,
        "sets": 3,
        "reps": 12,
        "goals": [
            {
            "target_sets": 4,
            "target_reps": 15
            }
        ]
        }
    ],
    "workout_goal": {
        "target_weight": 75.5
    }
    }
'''


workout_plan_summary = workout_ns.model('WorkoutPlanSummary', {
    'id': fields.Integer,
    'name': fields.String,
    'frequency': fields.String,
    'session_duration': fields.Integer,
    'created_at': fields.DateTime
})


@workout_ns.route('/summary')
class WorkoutPlanSummaryList(Resource):
    @workout_ns.marshal_list_with(workout_plan_summary)
    @workout_ns.doc(security='BearerAuth')
    @jwt_required()
    def get(self):
        """Get all workout plan summaries for current user"""
        user = User.get_current_user()
        if not user:
            return jsonify({"message": "User not found"}), 404

        plans = WorkoutPlan.query.filter_by(user_id=user.id).all()
        return [plan.to_summary() for plan in plans]


@workout_ns.route('')
class WorkoutPlanResource(Resource):
    @workout_ns.expect(workout_plan_model)
    @workout_ns.response(201, 'Workout plan created successfully', workout_plan_response)
    @workout_ns.response(400, 'Validation error')
    @workout_ns.response(404, 'User not found')
    @workout_ns.response(500, 'Server error')
    @jwt_required()
    def post(self):
        """Create a new workout plan with exercises and goals"""
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        data = workout_ns.payload

        # Validate required fields
        required_fields = ['name', 'selected_exercises', 'workout_goal']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        try:
            # Create workout plan
            workout_plan = WorkoutPlan(
                user_id=user.id,
                name=data['name'],
                frequency=data.get('frequency'),
                session_duration=data.get('session_duration')
            )
            db.session.add(workout_plan)
            db.session.flush()

            # Add exercises to plan
            for exercise_data in data['selected_exercises']:
                exercise = Exercises.query.get(
                    exercise_data.get('exercise_id'))
                if not exercise:
                    raise ValueError('Exercise not found')

                # Create selected exercise
                selected_exercise = SelectedExercise(
                    workout_plan_id=workout_plan.id,
                    exercise_id=exercise.id,
                    sets=exercise_data.get('sets'),
                    reps=exercise_data.get('reps'),
                    duration=exercise_data.get('duration'),
                    distance=exercise_data.get('distance')
                )
                db.session.add(selected_exercise)

            # Add workout goal
            workout_goal = WorkoutGoal(
                workout_plan_id=workout_plan.id,
                target_weight=float(data['workout_goal']['target_weight'])
            )
            db.session.add(workout_goal)

            db.session.commit()
            return workout_plan.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
