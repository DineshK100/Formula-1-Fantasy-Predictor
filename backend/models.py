from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user = db.Column(db.String(25), nullable=False)
    races = db.Column(db.String(500), nullable=False)
    points = db.Column(db.Integer, nullable=False)
