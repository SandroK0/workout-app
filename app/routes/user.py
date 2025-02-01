from flask import Blueprint, request, jsonify
from app import db
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return jsonify('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if user.chek_password(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
             datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Username not provided in the request.'}), 400

    existing_user = User.query.filter_by(name=data['name']).first()

    if existing_user:
        return jsonify({'message': 'Username already exists. Choose a different username.'}), 400

    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})
