from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models import WorkoutSession, User
from app import db


workout_sessions_ns = Namespace(
    'workout-sessions', description='Workout Sessions')

workout_session_model = workout_sessions_ns.model('WorkoutSession', {
    'workout_plan_id': fields.Integer(required=True, description='The ID of the workout plan'),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'date': fields.DateTime(required=True, description='The date of the workout session'),
    'duration': fields.Integer(required=True, description='Duration of the session in minutes'),
    'notes': fields.String(description='Notes about the session')
})


workout_session_model_response = workout_sessions_ns.model('WorkoutSessionResponse', {
    'id': fields.Integer(required=True, description='The unique identifier of the workout session'),
    'workout_plan_id': fields.Integer(required=True, description='The ID of the workout plan'),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'date': fields.DateTime(required=True, description='The date of the workout session'),
    'duration': fields.Integer(required=True, description='Duration of the session in minutes'),
    'notes': fields.String(description='Notes about the session')
})


@workout_sessions_ns.route("")
class WorkoutSessionList(Resource):
    """
    Resource for retrieving and creating workout sessions.
    """

    @workout_sessions_ns.response(200, "Success", [workout_session_model])
    @workout_sessions_ns.response(401, "Unauthorized")
    @workout_sessions_ns.response(404, "User not found")
    @jwt_required()
    def get(self):
        """
        Get a list of completed workout sessions for the authenticated user.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        sessions = WorkoutSession.query.filter_by(user_id=user.id).all()
        return {"workout_sessions": [session.to_dict() for session in sessions]}, 200

    @workout_sessions_ns.expect(workout_session_model)
    @workout_sessions_ns.response(201, "Workout session created successfully")
    @workout_sessions_ns.response(400, "Invalid input")
    @jwt_required()
    def post(self):
        """
        Create a new workout session for the authenticated user.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        data = workout_sessions_ns.payload
        if not data or "workout_plan_id" not in data or "duration" not in data:
            return {"message": "Invalid input"}, 400

        new_session = WorkoutSession(
            workout_plan_id=data.get('workout_plan_id'),
            user_id=user.id,
            duration=data.get('duration'),
            notes=data.get('notes')
        )
        db.session.add(new_session)
        db.session.commit()

        return {"message": "Workout session created successfully", "workout_session": new_session.to_dict()}, 201


@workout_sessions_ns.route("/<int:session_id>")
class SingleWorkoutSession(Resource):
    """
    Resource for retrieving a single workout session
    """

    @workout_sessions_ns.response(200, "Success")
    @workout_sessions_ns.response(404, "Workout session not found")
    @jwt_required()
    def get(self, session_id):
        """
        Retrieve a single completed workout session by ID, including exercises.
        """
        user = User.get_current_user()
        if not user:
            return {"message": "User not found"}, 404

        session = WorkoutSession.query.filter_by(id=session_id, user_id=user.id).first()
        if not session:
            return {"message": "Workout session not found"}, 404

        return {
            "workout_session": session.to_dict(),
        }, 200
