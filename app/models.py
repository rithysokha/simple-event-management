from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(100))
    guests = db.relationship("Guest", back_populates="event")

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(100))
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="guests")
    
