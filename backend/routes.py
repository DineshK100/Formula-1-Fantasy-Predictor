from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route("/")
def home():
    return {"message": "Hello starting the website"}

@bp.route("/predict")
def predict():
    return {"message": "Hello starting the prediction"}
