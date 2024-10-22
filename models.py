from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, default=0)
    last_claim_time = db.Column(db.DateTime)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timer_duration = db.Column(db.Integer, default=60) 
    coins_per_click = db.Column(db.Integer, default=1)
