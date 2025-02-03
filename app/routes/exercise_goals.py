from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models import Exercises, User, ExerciseGoal
from app import db


exercises_goals_ns = Namespace('exercise-goals', description='Exercise Goals')

exercise_model = exercises_goals_ns.model('Exercise', {
    'id': fields.Integer(required=True, description='The unique identifier of the exercise'),
    'name': fields.String(required=True, description='The name of the exercise'),
    'description': fields.String(required=True, description='A description of the exercise'),
    'instructions': fields.String(required=True, description='Instructions for the exercise'),
    'target_muscles': fields.String(required=True, description='Target muscles'),
    'difficulty': fields.Integer(required=True, description='Difficulty of the exercise')
})


exercise_goal_model = exercises_goals_ns.model('ExerciseGoal', {
    'exercise_id': fields.Integer(required=True, description='The ID of the exercise'),
    'target_sets': fields.Integer(description='The target number of sets'),
    'target_reps': fields.Integer(description='The target number of reps'),
    'target_duration': fields.String(description='The target duration'),
    'target_distance': fields.String(description='The target distance')
})


@exercises_goals_ns.route("")
class ExerciseGoalsList(Resource):
    """
    Resource for managing exercise goals.
    """

    @exercises_goals_ns.response(200, "Success", [exercise_model])
    @exercises_goals_ns.response(401, "Unauthorized")
    @exercises_goals_ns.response(404, "User not found")
    @jwt_required()
    def get(self):
        """
        Get a list of exercise goals for the authenticated user.

        Returns:
            200: A list of exercise goals.
            401: Unauthorized access.
            404: If the user is not found.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        exercise_goals = ExerciseGoal.query.filter_by(user_id=user.id).all()
        return {"exercise_goals": [exercise_goal.to_dict() for exercise_goal in exercise_goals]}, 200

    @exercises_goals_ns.expect(exercise_goal_model)
    @exercises_goals_ns.response(201, "Exercise goal created successfully")
    @exercises_goals_ns.response(400, "Invalid input")
    @exercises_goals_ns.response(401, "Unauthorized")
    @exercises_goals_ns.response(404, "User not found")
    @jwt_required()
    def post(self):
        """
        Create a new exercise goal for the authenticated user.

        Returns:
            201: Exercise goal created successfully.
            400: If request data is invalid.
            401: Unauthorized access.
            404: If the user is not found.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        data = exercises_goals_ns.payload

        if not data or "exercise_id" not in data:
            return {"message": "Invalid input"}, 400

        exercise = Exercises.query.get(data.get('exercise_id'))
        if not exercise:
            return {"message": "Exercise not found"}, 404

        new_goal = ExerciseGoal(exercise_id=exercise.id, user_id=user.id, target_sets=data.get('target_sets'), target_reps=data.get(
            'target_reps'), target_duration=data.get('target_duration'), target_distance=data.get('target_distance'))
        db.session.add(new_goal)
        db.session.commit()

        return {"message": "Exercise goal created successfully", "exercise_goal": new_goal.to_dict()}, 201


@exercises_goals_ns.route("/<int:exercise_goal_id>")
class SingleExerciseGoal(Resource):
    """
    Resource for handling a single exercise goal.
    """

    @exercises_goals_ns.response(200, "Success")
    @exercises_goals_ns.response(404, "Exercise goal not found")
    @jwt_required()
    def get(self, exercise_goal_id):
        """
        Retrieve a single exercise goal by ID.
        """

        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        exercise_goal = ExerciseGoal.query.filter_by(
            id=exercise_goal_id, user_id=user.id).first()
        if not exercise_goal:
            return {"message": "Exercise goal not found"}, 404

        return exercise_goal.to_dict(), 200

    @exercises_goals_ns.expect(exercise_goal_model)
    @exercises_goals_ns.response(200, "Exercise goal updated successfully")
    @exercises_goals_ns.response(400, "Invalid input")
    @exercises_goals_ns.response(404, "Exercise goal not found")
    @jwt_required()
    def put(self, exercise_goal_id):
        """
        Update an existing exercise goal.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        exercise_goal = ExerciseGoal.query.filter_by(
            id=exercise_goal_id, user_id=user.id).first()
        if not exercise_goal:
            return {"message": "Exercise goal not found"}, 404

        data = exercises_goals_ns.payload
        if not data:
            return {"message": "Invalid input"}, 400

        for key, value in data.items():
            setattr(exercise_goal, key, value)

        db.session.commit()
        return {"message": "Exercise goal updated successfully", "exercise_goal": exercise_goal.to_dict()}, 200

    @exercises_goals_ns.response(200, "Exercise goal deleted successfully")
    @exercises_goals_ns.response(404, "Exercise goal not found")
    @jwt_required()
    def delete(self, exercise_goal_id):
        """
        Delete an existing exercise goal.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        exercise_goal = ExerciseGoal.query.filter_by(
            id=exercise_goal_id, user_id=user.id).first()
        if not exercise_goal:
            return {"message": "Exercise goal not found"}, 404

        db.session.delete(exercise_goal)
        db.session.commit()
        return {"message": "Exercise goal deleted successfully"}, 200
