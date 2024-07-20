from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from .prediction import main
from .fantasy import main as mainFantasy
from .models import db, User

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return "Hello Home page"

@bp.route("/predict", methods=['POST'])
def predict():
    race = request.get_json(force=True)
    podiumPrediction = main(race["race"])
    return jsonify(podiumPrediction)

@bp.route("/fantasy", methods=['POST'])
def fantasy():
    race = request.get_json(force=True)
    fantasyPredictions = mainFantasy(race["race"])
    return jsonify(fantasyPredictions)

@bp.route("/signup", methods=['POST'])
def signup():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"success": False, "message": "Data must be entered"}), 400
    
    username = data.get('username')
    email = data.get('email')
    
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords don't match!"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(seconds=150)}, 
                       "5f00cab06c38701cc5c5dfdc06b7e2c8272c9304902967248351d273970c036f", algorithm="HS256")

    return jsonify({'token': token, "success": True})

if __name__ == "__main__":
    bp.run(debug=True)
