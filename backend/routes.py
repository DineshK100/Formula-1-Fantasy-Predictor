from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from .prediction import main
from .fantasy import main as mainFantasy
from .models import db, User, Stats

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

    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(days=7)}, 
                       "5f00cab06c38701cc5c5dfdc06b7e2c8272c9304902967248351d273970c036f", algorithm="HS256")

    return jsonify({'token': token, "success": True})

@bp.route("/stats", methods=['POST'])
def stats():
    data = request.get_json(force=True)
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"success": False, "message": "Authorization header missing"}), 400

    token = auth_header.split()[1]
    username = jwt.decode(token, "5f00cab06c38701cc5c5dfdc06b7e2c8272c9304902967248351d273970c036f", algorithms=["HS256"])
    user = username['user']
    
    race = data.get('race')
    points = data.get('points')
    
    if not race or points is None:
        return jsonify({"success": False, "message": "Race and points must be provided"}), 400
    
    new_entry = Stats(user= user, races=race, points=points)
    db.session.add(new_entry)
    db.session.commit()
    
    user_stats = Stats.query.filter_by(user=user).all()
    stats = [{"race": stat.races, "points": stat.points} for stat in user_stats]
    
    return jsonify({"success": True, "message": "Data added successfully", "stats": stats})



@bp.route("/login", methods=['POST'])
def login():
    data = request.get_json(force=True)
    
    if not data:
        return jsonify({"success": False, "message": "Data must be entered"}), 400
    
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid username or password"}), 400

    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(days=7)}, 
                       "5f00cab06c38701cc5c5dfdc06b7e2c8272c9304902967248351d273970c036f", algorithm="HS256")

    return jsonify({'token': token, "success": True})

if __name__ == "__main__":
    bp.run(debug=True)