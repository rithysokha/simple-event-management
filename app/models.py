from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    events = db.relationship("Event", back_populates="user")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.String(100))
    location = db.Column(db.String(100))
    guests = db.relationship("Guest", back_populates="event")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="events")

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="guests")
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id')) 
    gender = db.relationship("Gender", back_populates="guests") 


class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    guests = db.relationship("Guest", back_populates="gender") 