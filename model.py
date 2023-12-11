from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    age = db.Column(db.Integer)