from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:dineshandsam@localhost/mydatabase'
    app.config['JWT_SECRET_KEY'] = '5f00cab06c38701cc5c5dfdc06b7e2c8272c9304902967248351d273970c036f'

    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
