from flask import jsonify
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(90))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_current_user():
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if not user:
            return None, jsonify({"message": "User not found"}), 404
        return user, None


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    blacklisted_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class Exercises(db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    target_muscles = db.Column(db.String(255))
    difficulty = db.Column(db.Integer)

    def to_dict(self):
        return {
            'exercise_id': self.exercise_id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'target_muscles': self.target_muscles,
            'difficulty': self.difficulty
        }


class WorkoutPlanFinal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(50))
    goal = db.Column(db.String(255))
    session_duration = db.Column(db.Integer)
    selected_exercises = db.Column(db.String(5000))


class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.String(50), nullable=False)
    workout_plan_id = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String(255), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    rest_time = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workout_plan_id': self.workout_plan_id,
            'exercise_name': self.exercise_name,
            'sets': self.sets,
            'reps': self.reps,
            'completed': self.completed,
            'rest_time': self.rest_time
        }


class FitnessGoalsFinal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    current_weight = db.Column(db.Float, nullable=False)
    weight_goal = db.Column(db.Float, nullable=False)
    exercise_goals = db.relationship(
        'ExerciseGoal', backref='fitness_goal', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'current_weight': self.current_weight,
            'weight_goal': self.weight_goal,
            'exercise_goals': [exercise_goal.to_dict() for exercise_goal in self.exercise_goals]
        }


class ExerciseGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fitness_goal_id = db.Column(db.Integer, db.ForeignKey(
        'fitness_goals_final.id'), nullable=False)
    exercise_name = db.Column(db.String(255), nullable=False)
    current_weight = db.Column(db.Float)
    current_reps = db.Column(db.Integer)
    target_weight = db.Column(db.Float)
    target_reps = db.Column(db.Integer)

    def to_dict(self):
        return {
            'exercise_name': self.exercise_name,
            'current_weight': self.current_weight,
            'current_reps': self.current_reps,
            'target_weight': self.target_weight,
            'target_reps': self.target_reps
        }
