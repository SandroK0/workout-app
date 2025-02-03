from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, SelectedExercise, User, Exercises
from app import db


workout_plans_ns = Namespace(
    'workout-plans', description='Workout Plans Operations')


exercise_model_response = workout_plans_ns.model('Exercise', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'instructions': fields.String,
    'target_muscles': fields.String,
    'difficulty': fields.Integer,
})


# Model for selected exercises
selected_exercise_response = workout_plans_ns.model('SelectedExerciseResponse', {
    'id': fields.Integer(required=True),
    'exercise': fields.Nested(exercise_model_response),
    'sets': fields.Integer,
    'reps': fields.Integer,
    'duration': fields.String,
    'distance': fields.String,
})

# Model for selected exercises
selected_exercise_model = workout_plans_ns.model('SelectedExercise', {
    'exersize-id': fields.Integer(required=True),
    'sets': fields.Integer,
    'reps': fields.Integer,
    'duration': fields.String,
    'distance': fields.String,
})

# Main workout plan model
workout_plan_model = workout_plans_ns.model('WorkoutPlan', {
    'name': fields.String(required=True),
    'frequency': fields.String,
    'session_duration': fields.Integer,
    'selected_exercises': fields.List(fields.Nested(selected_exercise_model), required=True),
})


# Response model
workout_plan_response = workout_plans_ns.model('WorkoutPlanResponse', {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'frequency': fields.String,
    'session_duration': fields.Integer,
    'selected_exercises': fields.List(fields.Nested(selected_exercise_response)),
})


workout_plan_summary_response = workout_plans_ns.model('WorkoutPlanSummaryResponse', {
    'id': fields.Integer,
    'name': fields.String,
    'frequency': fields.String,
    'session_duration': fields.Integer,
})


workout_plan_summary = workout_plans_ns.model('WorkoutPlanSummary', {
    'name': fields.String,
    'frequency': fields.String,
    'session_duration': fields.Integer,
})


@workout_plans_ns.route('/summary')
class WorkoutPlanSummaryList(Resource):
    @workout_plans_ns.response(200, 'Workout plan created successfully', workout_plan_summary_response)
    @jwt_required()
    def get(self):
        """Get all workout plan summaries for current user"""
        user = User.get_current_user()
        if not user:
            return jsonify({"message": "User not found"}), 404

        plans = WorkoutPlan.query.filter_by(user_id=user.id).all()
        return [plan.to_summary() for plan in plans]


@workout_plans_ns.route('')
class WorkoutPlanResource(Resource):
    @workout_plans_ns.expect(workout_plan_model)
    @workout_plans_ns.response(201, 'Workout plan created successfully', workout_plan_response)
    @workout_plans_ns.response(400, 'Validation error')
    @workout_plans_ns.response(404, 'User not found')
    @workout_plans_ns.response(500, 'Server error')
    @jwt_required()
    def post(self):
        """Create a new workout plan with exercises"""
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        data = workout_plans_ns.payload

        # Validate required fields
        required_fields = ['name', 'selected_exercises']
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

            db.session.commit()
            return {'message': 'Workout plan created successfully', 'workout_plan': workout_plan.to_dict()}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400


@workout_plans_ns.route('/<int:plan_id>')
@workout_plans_ns.doc(params={"plan_id": "The ID of the workout plan"})
class SingleWorkoutPlanResource(Resource):
    """
    Resource for managing a single workout plan.
    Allows retrieving and deleting a workout plan owned by the authenticated user.
    """

    @workout_plans_ns.response(200, "Success", workout_plan_response)
    @workout_plans_ns.response(404, "Workout plan not found")
    @jwt_required()
    def get(self, plan_id):
        """
        Get a specific workout plan by its ID.

        Retrieves a workout plan that belongs to the authenticated user.

        **Returns:**
        - 200: A JSON object representing the workout plan.
        - 404: If the workout plan does not exist or does not belong to the user.
        """
        plan = self._get_user_plan(plan_id)

        return plan.to_dict()

    @workout_plans_ns.response(204, "Workout plan deleted successfully")
    @workout_plans_ns.response(400, "Error deleting workout plan")
    @workout_plans_ns.response(404, "Workout plan not found")
    @jwt_required()
    def delete(self, plan_id):
        """
        Delete a workout plan.

        Deletes a workout plan that belongs to the authenticated user.

        **Returns:**
        - 204: If the workout plan is deleted successfully.
        - 400: If there is an error during deletion.
        - 404: If the workout plan does not exist or does not belong to the user.
        """
        plan = self._get_user_plan(plan_id)

        try:
            db.session.delete(plan)
            db.session.commit()
            return "", 204
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    @workout_plans_ns.expect(workout_plan_summary)
    @workout_plans_ns.response(200, "Workout plan updated successfully", workout_plan_summary_response)
    @workout_plans_ns.response(400, "Validation error")
    @workout_plans_ns.response(404, "Workout plan not found")
    @jwt_required()
    def put(self, plan_id):
        """
        Update an existing workout plan.

        Updates a workout plan that belongs to the authenticated user.

        **Returns:**
        - 200: The updated workout plan.
        - 400: If there is a validation error.
        - 404: If the workout plan does not exist or does not belong to the user.
        """
        plan = self._get_user_plan(plan_id)
        data = workout_plans_ns.payload

        try:
            plan.name = data.get('name', plan.name)
            plan.frequency = data.get('frequency', plan.frequency)
            plan.session_duration = data.get(
                'session_duration', plan.session_duration)

            db.session.commit()
            return {'message': 'Workout plan updated successfully', 'workout_plan': plan.to_dict()}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    def _get_user_plan(self, plan_id):
        """
        Helper function to fetch a workout plan and verify ownership.

        **Returns:**
        - The workout plan object if found.
        - Aborts with 404 if the plan does not exist or does not belong to the user.
        """
        user = User.get_current_user()
        if not user:
            workout_plans_ns.abort(404, "User not found")

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            workout_plans_ns.abort(404, "Workout plan not found")
        return plan
