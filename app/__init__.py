from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()



authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    version='1.0',
    title='Workout App API',
    description='API for the Workout App',
    authorizations=authorizations,
    security='BearerAuth'  # Apply globally
)

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///workout.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    if not app.config['JWT_SECRET_KEY']:
        raise ValueError("JWT_SECRET_KEY is not set in the environment!")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize API
    api.init_app(app)

    # Register namespaces
    from .routes.user import user_ns
    from .routes.exercises import exercises_ns
    api.add_namespace(user_ns, path='/api/user')
    api.add_namespace(exercises_ns, path='/api/exercises')

    return app