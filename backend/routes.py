from flask import Blueprint, jsonify, request
import requests
from .prediction import main
from .fantasy import main as mainFantasy

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return "Hello Home page"

@bp.route("/predict", methods = ['POST', 'GET'])
def predict():
    race = request.get_json(force = "true")
    podiumPrediction = main(race["race"])
    return jsonify(podiumPrediction)

@bp.route("/fantasy", methods = ['POST', 'GET'])
def fantasy():
    fantasyPredictions = mainFantasy()
    # fantasyPredictions['drivers'] = [(driver, int(price), int(points)) for driver, price, points in fantasyPredictions['drivers']]
    # fantasyPredictions['constructors'] = [(constructor, int(price), int(points)) for constructor, price, points in fantasyPredictions['constructors']]
    return jsonify(fantasyPredictions)

@bp.route("/signup")
def signup():
    return "Hello starting the sign up page"

if __name__ == "__main__":
    bp.run(debug=True)