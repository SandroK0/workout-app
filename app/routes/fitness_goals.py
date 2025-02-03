from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import  jwt_required
from app import db
from app.models import User, FitnessGoal

fitness_goals_ns = Namespace('fitness-goals', description='Fitness Goals')

fitness_goal_model = fitness_goals_ns.model('FitnessGoal', {
    'target_weight': fields.Float(required=True, description='The target weight of the user'),
    'target_body_fat_percentage': fields.Float(required=True, description='The target body fat percentage of the user'),
    'target_muscle_mass': fields.Float(required=True, description='The target muscle mass of the user')
})


@fitness_goals_ns.route('')
class FitnessGoalResource(Resource):

    @jwt_required()
    @fitness_goals_ns.response(200, 'Fitness Goal retrieved successfully', fitness_goal_model)
    @fitness_goals_ns.response(401, 'Unauthorized')
    @fitness_goals_ns.response(404, 'User not found')
    def get(self):
        """Get current user's profile information"""
        current_user = User.get_current_user()

        if not current_user or not current_user.fitness_goal:
            return {"error": "User not found"}, 404

        return {
            "message": "Fitness Goal retrieved successfully",
            "profile": current_user.fitness_goal.to_dict()
        }, 200

    @jwt_required()
    @fitness_goals_ns.expect(fitness_goal_model)
    @fitness_goals_ns.response(200, "Fitness Goal updated successfully")
    @fitness_goals_ns.response(400, "Invalid input data")
    @fitness_goals_ns.response(401, "Unauthorized")
    @fitness_goals_ns.response(404, "User not found")
    def put(self):
        """Update user profile information"""
        current_user = User.get_current_user()

        if not current_user or not current_user.profile:
            return {"error": "User not found"}, 404

        data = fitness_goals_ns.payload 
        fitness_goal = FitnessGoal.query.filter_by(user_id=current_user.id).first()

        fields_to_update = [
            "target_weight",
            "target_body_fat_percentage", "target_muscle_mass"
        ]

        try:
            for field in fields_to_update:
                if field in data and data[field] is not None:
                    setattr(fitness_goal, field, data[field])

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

        return {
            "message": "Fitness Goal updated successfully",
            "profile": fitness_goal.to_dict()
        }, 200
