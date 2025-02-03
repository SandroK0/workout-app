from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, SelectedExercise, User, Exercises
from app import db


workout_plans_exercise_ns = Namespace(
    'workout-plans-exercises', description='Workout Plans Exercises')


exercise_model_response = workout_plans_exercise_ns.model('Exercise', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'instructions': fields.String,
    'target_muscles': fields.String,
    'difficulty': fields.Integer,
})


# Model for selected exercises
selected_exercise_response = workout_plans_exercise_ns.model('SelectedExerciseResponse', {
    'id': fields.Integer(required=True),
    'exercise': fields.Nested(exercise_model_response),
    'sets': fields.Integer,
    'reps': fields.Integer,
    'duration': fields.String,
    'distance': fields.String,
})

# Model for selected exercises
selected_exercise_model = workout_plans_exercise_ns.model('SelectedExercise', {
    'exercise_id': fields.Integer(required=True),
    'sets': fields.Integer,
    'reps': fields.Integer,
    'duration': fields.String,
    'distance': fields.String,
})


@workout_plans_exercise_ns.route('/<int:plan_id>/exercises')
class WorkoutPlanExercisesListResource(Resource):
    """
        Allows adding and fetching exercises in a workout plan.
    """

    @workout_plans_exercise_ns.response(200, 'Exercises retrieved successfully')
    @workout_plans_exercise_ns.response(404, 'Workout plan not found')
    @jwt_required()
    def get(self, plan_id):
        """
        Retrieve all exercises in a specific workout plan.

        **Parameters:**
        - `plan_id`: The ID of the workout plan.

        **Returns:**
        - 200: A list of exercises in the workout plan.
        - 404: If the workout plan does not exist.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            return {"message": "Workout plan not found"}, 404

        exercises = SelectedExercise.query.filter_by(
            workout_plan_id=plan.id).all()

        return {"exercises": [exercise.to_dict() for exercise in exercises]}, 200

    @workout_plans_exercise_ns.expect(selected_exercise_model)
    @workout_plans_exercise_ns.response(201, 'Exercise added to workout plan successfully', selected_exercise_response)
    @workout_plans_exercise_ns.response(400, 'Validation error')
    @workout_plans_exercise_ns.response(404, 'Workout plan or exercise not found')
    @jwt_required()
    def post(self, plan_id):
        """
        Add a new exercise to a workout plan.

        **Parameters:**
        - `plan_id`: The ID of the workout plan to which the exercise will be added.

        **Request Body:**
        - `exercise_id`: The ID of the exercise to add.
        - `sets`: Number of sets.
        - `reps`: Number of reps.
        - `duration`: Duration of the exercise (optional).
        - `distance`: Distance for the exercise (optional).

        **Returns:**
        - 201: The added exercise.
        - 400: If there is a validation error.
        - 404: If the workout plan or exercise does not exist.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            return {"message": "Workout plan not found"}, 404

        data = workout_plans_exercise_ns.payload

        try:
            print("exercise_id", data.get('exercise_id'))
            exercise = Exercises.query.get(data.get('exercise_id'))
            if not exercise:
                return {"message": "Exercise not found"}, 404

            selected_exercise = SelectedExercise(
                workout_plan_id=plan.id,
                exercise_id=exercise.id,
                sets=data.get('sets'),
                reps=data.get('reps'),
                duration=data.get('duration'),
                distance=data.get('distance')
            )
            db.session.add(selected_exercise)
            db.session.commit()

            return {"message": "Exercise added successfully", "exercise": selected_exercise.to_dict()}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400


@workout_plans_exercise_ns.route('/<int:plan_id>/exercise/<int:id>')
class WorkoutPlanExerciseResource(Resource):
    """
    Resource to manage an exercise from a specific workout plan.
    """

    @workout_plans_exercise_ns.response(200, 'Exercise retrieved successfully', selected_exercise_response)
    @workout_plans_exercise_ns.response(404, 'Workout plan or exercise not found')
    @jwt_required()
    def get(self, plan_id, id):
        """
        Retrieve details of an exercise in a specific workout plan.

        **Parameters:**
        - `plan_id`: The ID of the workout plan.
        - `id`: The ID of the selected exercise.

        **Returns:**
        - 200: The requested exercise details.
        - 404: If the workout plan or exercise does not exist.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            return {"message": "Workout plan not found"}, 404

        selected_exercise = SelectedExercise.query.filter_by(
            id=id, workout_plan_id=plan.id
        ).first()

        if not selected_exercise:
            return {"message": "Selected exercise not found in this workout plan"}, 404

        return {"exercise": selected_exercise.to_dict()}, 200

    @workout_plans_exercise_ns.expect(selected_exercise_model)
    @workout_plans_exercise_ns.response(200, 'Exercise updated successfully', selected_exercise_response)
    @workout_plans_exercise_ns.response(400, 'Validation error')
    @workout_plans_exercise_ns.response(404, 'Workout plan or exercise not found')
    @jwt_required()
    def put(self, plan_id, id):
        """
        Update an exercise in a specific workout plan.

        **Parameters:**
        - `plan_id`: The ID of the workout plan.
        - `id`: The ID of the selected exercise to update.

        **Request Body:**
        - `sets`: Number of sets (optional).
        - `reps`: Number of reps (optional).
        - `duration`: Duration of the exercise (optional).
        - `distance`: Distance for the exercise (optional).

        **Returns:**
        - 200: The updated exercise.
        - 400: If there is a validation error.
        - 404: If the workout plan or exercise does not exist.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            return {"message": "Workout plan not found"}, 404

        selected_exercise = SelectedExercise.query.filter_by(
            id=id, workout_plan_id=plan.id
        ).first()

        if not selected_exercise:
            return {"message": "Selected exercise not found in this workout plan"}, 404

        data = workout_plans_exercise_ns.payload

        try:
            if "sets" in data:
                selected_exercise.sets = data["sets"]
            if "reps" in data:
                selected_exercise.reps = data["reps"]
            if "duration" in data:
                selected_exercise.duration = data["duration"]
            if "distance" in data:
                selected_exercise.distance = data["distance"]

            db.session.commit()

            return {"message": "Exercise updated successfully", "exercise": selected_exercise.to_dict()}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400

    @workout_plans_exercise_ns.response(204, 'Exercise deleted successfully')
    @workout_plans_exercise_ns.response(400, 'Error deleting exercise')
    @workout_plans_exercise_ns.response(404, 'Workout plan or exercise not found')
    @jwt_required()
    def delete(self, plan_id, id):
        """
        Delete an exercise from a specific workout plan.

        **Parameters:**
        - `plan_id`: The ID of the workout plan.
        - `id`: The ID of the selected exercise to delete.

        **Returns:**
        - 204: If the exercise is deleted successfully.
        - 400: If there is an error during deletion.
        - 404: If the workout plan or exercise does not exist.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=user.id).first()
        if not plan:
            return {"message": "Workout plan not found"}, 404

        selected_exercise = SelectedExercise.query.filter_by(
            id=id, workout_plan_id=plan.id
        ).first()

        if not selected_exercise:
            return {"message": "Selected exercise not found in this workout plan"}, 404

        try:
            db.session.delete(selected_exercise)
            db.session.commit()
            return "", 204

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400
