from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return "Hello starting the website"

@bp.route("/predict")
def predict():
    return {"message": "Hello starting the prediction"}


@bp.route("/fantasy")
def fantasy():
    return "Hello starting the fantasy prediction"

if __name__ == "__main__":
    bp.run(debug=True)