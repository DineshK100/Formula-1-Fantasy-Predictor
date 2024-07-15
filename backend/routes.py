from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return "Hello Home page"

@bp.route("/predict")
def predict():
    return {"message": "Hello starting the prediction"}

@bp.route("/fantasy")
def fantasy():
    return "Hello starting the fantasy prediction"

@bp.route("/signup")
def fantasy():
    return "Hello starting the sign up page"


if __name__ == "__main__":
    bp.run(debug=True)