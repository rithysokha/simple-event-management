from flask_restx import Namespace, Resource

from .extensions import db
from .models import *
from .api_models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

authorizations = {
    "jsonWebToken":{
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace('api', authorizations=authorizations)
uns = Namespace('auth', authorizations=authorizations)
no_event_fount_message = 'No event found'
no_guest_found_message = 'No guest found'
# USER
@uns.route('/signup')
class Users(Resource):
    @uns.expect(user_input_model)
    def post(self):
        """Create a new user"""
        user_input = User(username=ns.payload['username'], password_hash=generate_password_hash(ns.payload['password']))
        db.session.add(user_input)
        db.session.commit()
        return 'Sign up succeful', 201

@uns.route('/login')
class Login(Resource):
    @uns.expect(user_login_model)
    def post(self):
        """Login a user"""
        user_input = User.query.filter_by(username=ns.payload['username']).first()
        if user_input and check_password_hash(user_input.password_hash, ns.payload['password']):
            return {'access_token': create_access_token(identity=user_input.id)}, 200
        else: return {'message': 'Invalid username or password'}, 401
    

# EVENT
@ns.route('/events')
class Events(Resource):
    @ns.doc(security='jsonWebToken')
    @jwt_required()
    @ns.marshal_list_with(event_output_model)
    def get(self):
        """Get all events"""
        event_output = Event.query.filter_by(user_id = get_jwt_identity()).all()
        if event_output:
            return event_output
        else: return {'message': no_event_fount_message}, 404

    @ns.expect(event_intput_model)
    @ns.marshal_with(event_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def post(self):
        """Create a new event"""
        event_input = Event(name=ns.payload['name'], date=ns.payload['date'], location=ns.payload['location'], user_id =get_jwt_identity())
        db.session.add(event_input)
        db.session.commit()
        return event_input, 201

# a single event
@ns.route('/events/<int:eid>')
class OneEvent(Resource):
    @ns.marshal_with(event_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def get(self, eid):
        """Get a single event"""
        event_output = Event.query.filter_by(user_id = get_jwt_identity(), id = eid).first()
        if event_output:
            return event_output
        else: return {'message': no_event_fount_message}, 404

    @ns.expect(event_update_model)
    @ns.marshal_with(event_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def put(self, id):
        """Update a single event"""
        event_output = Event.query.get(id)
        if(event_output):
            event_output.name = ns.payload['name']
            event_output.date = ns.payload['date']
            event_output.location = ns.payload['location']
            db.session.commit()
            return event_output
        else: return {'message': no_event_fount_message}, 404
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def delete(self, id):
        """Delete a single event"""
        event_output = Event.query.get(id)
        if event_output: 
            db.session.delete(event_output)
            db.session.commit()
            return {'message': 'Event deleted'}, 200
        else: return {'message': no_event_fount_message}, 404

#  all guests for a single event
@ns.route('/events/<int:id>/guests')
class Guests(Resource):
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(guest_output_model)
    def get(self, id):
        """Get all guests for a single event"""
        guests_output = Guest.query.filter_by(event_id=id).all()  
        if guests_output:
            return guests_output
        else: return {'message': no_guest_found_message}, 404


#GENDER 
@ns.route('/genders')
class Genderss(Resource):
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(gender_output_model)
    def get(self):
        genderr = Gender.query.all()
        if genderr:
            return genderr
        else: return "nothing found"
    
    @ns.expect(gender_input_model)
    @ns.marshal_with(gender_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def post(self):
        gender = Gender(**ns.payload)
        db.session.add(gender)
        db.session.commit()
        return gender, 201
    
@ns.route('/genders/<int:id>')
class OneGender(Resource):
    @ns.expect(gender_input_model)
    @ns.marshal_with(gender_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def put(self, id):
        gender = Gender.query.get(id)
        if gender:
            gender.name = ns.payload['name']
            db.session.commit()
            return "Gender updated", 200
        else: return "nothing found", 404
    
    def delete(self, id):
        db.session.delete(Gender.query.get(id))
        db.session.commit()

# GUEST
@ns.route('/guests')
class GetAllGuests(Resource):
    @ns.marshal_list_with(guest_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def get(self):
        """Get all guests"""
        guests_output = Guest.query.all()
        if guests_output:
            return guests_output
        else: return {'message': no_guest_found_message}, 404

    @ns.expect(guest_input_model)
    @ns.marshal_with(guest_input_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def post(self):
        """Create a new guest"""
        guest_input = Guest(name=ns.payload['name'], gender_id = ns.payload['gender_id'], event_id = ns.payload['event_id'])
        db.session.add(guest_input)
        db.session.commit()
        return guest_input, 201
@ns.route('/guests/<int:id>')
class OneGuest(Resource):
    @ns.expect(guest_input_model)
    @ns.marshal_with(guest_output_model)
    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def put(self, id):
        """Update a single guest"""
        guest = Guest.query.get(id)
        if guest:
            guest.name = ns.payload['name']
            guest.gender= ns.payload['gender']
            guest.event_id = ns.payload['event_id']
            db.session.commit()
            return guest
        else: return {'message': no_guest_found_message}, 404

    @jwt_required()
    @ns.doc(security='jsonWebToken')
    def delete(self, id):
        """Delete a single guest"""
        guest = Guest.query.get(id)
        if guest:
            db.session.delete(guest)
            db.session.commit()
            return {'message': 'Guest deleted'}, 200
        else: return {'message': no_guest_found_message}, 404
