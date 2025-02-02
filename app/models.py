from flask import jsonify
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(90), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_current_user():
        current_user_id = get_jwt_identity()
        return User.query.get(int(current_user_id))

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    current_weight = db.Column(db.Float)
    target_weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    body_fat_percentage = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'current_weight': self.current_weight,
            'target_weight': self.target_weight,
            'height': self.height,
            'age': self.age,
            'body_fat_percentage': self.body_fat_percentage,
            'muscle_mass': self.muscle_mass,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Exercises(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    target_muscles = db.Column(db.String(255))
    difficulty = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'target_muscles': self.target_muscles,
            'difficulty': self.difficulty
        }

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(50))
    session_duration = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('workout_plans', cascade='all, delete-orphan'))
    selected_exercises = db.relationship('SelectedExercise', backref='workout_plan', cascade='all, delete-orphan')
    workout_goal = db.relationship('WorkoutGoal', backref='workout_plan', cascade='all, delete-orphan', uselist=False)

class SelectedExercise(db.Model):
    __tablename__ = 'selected_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False, index=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration = db.Column(db.String(100))
    distance = db.Column(db.String(100))

    exercise = db.relationship('Exercises', backref=db.backref('selections', cascade='all, delete-orphan'))

class WorkoutGoal(db.Model):
    __tablename__ = 'workout_goals'

    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    target_weight = db.Column(db.Float, nullable=False)

class ExerciseGoal(db.Model):
    __tablename__ = 'exercise_goals'

    id = db.Column(db.Integer, primary_key=True)
    selected_exercise_id = db.Column(db.Integer, db.ForeignKey('selected_exercises.id', ondelete='CASCADE'), nullable=False, index=True)
    target_sets = db.Column(db.Integer, nullable=False)
    target_reps = db.Column(db.Integer, nullable=False)
    target_duration = db.Column(db.String(50))
    target_distance = db.Column(db.String(50))

    selected_exercise = db.relationship('SelectedExercise', backref=db.backref('goals', cascade='all, delete-orphan'))

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'

    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('sessions', cascade='all, delete-orphan'))
    workout_plan = db.relationship('WorkoutPlan', backref=db.backref('sessions', cascade='all, delete-orphan'))

class WorkoutSessionExercise(db.Model):
    __tablename__ = 'workout_session_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    selected_exercise_id = db.Column(db.Integer, db.ForeignKey('selected_exercises.id', ondelete='CASCADE'), nullable=False, index=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration = db.Column(db.String(50))
    distance = db.Column(db.String(50))

    selected_exercise = db.relationship('SelectedExercise', backref=db.backref('session_exercises', cascade='all, delete-orphan'))