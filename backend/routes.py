from flask import Blueprint, jsonify, request
from .prediction import main
from .fantasy import main as mainFantasy

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return "Hello Home page"

@bp.route("/predict", methods = ['POST', 'GET'])
def predict():
    race = request.form["race"]
    podiumPrediction = main(race)
    return jsonify(podiumPrediction)

@bp.route("/fantasy")
def fantasy():
    fantasyPredictions = mainFantasy() 
    return jsonify(fantasyPredictions)

@bp.route("/signup")
def signup():
    return "Hello starting the sign up page"


if __name__ == "__main__":
    bp.run(debug=True)