from flask_restx import Namespace, Resource

from .extensions import db
from .models import Guest, User, Gender, Event
from .api_models import event_output_model, event_intput_model, guest_output_model, guest_input_model, gender_output_model
from flask_jwt_extended import jwt_required, get_jwt_identity

authorizations = {
    "jsonWebToken":{
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace('api', authorizations=authorizations)

@ns.route('/events')
class Events(Resource):
    @ns.marshal_list_with(event_output_model)
    def get(self):
        """Get all events"""
        event_output = Event.query.all()
        if event_output:
            return event_output
        else: return {'message': 'No events found'}, 404

    @ns.expect(event_intput_model)
    @ns.marshal_with(event_output_model)
    def post(self):
        """Create a new event"""
        event_input = Event(**ns.payload)
        db.session.add(event_input)
        db.session.commit()
        return event_input, 201

# a single event
@ns.route('/events/<int:id>')
class OneEvent(Resource):
    @ns.marshal_with(event_output_model)
    def get(self, id):
        """Get a single event"""
        event_output = Event.query.get(id)
        if event_output:
            return event_output
        else: return {'message': 'No event found'}, 404

    @ns.expect(event_intput_model)
    @ns.marshal_with(event_output_model)
    def put(self, id):
        """Update a single event"""
        event_output = Event.query.get(id)
        if(event_output):
            if(ns.payload['name'] != "String"):
                event_output.name = ns.payload['name']
            else: event_output.name = Event.query.get(id).name
            if(ns.payload['date'] != "String"):    
                event_output.date = ns.payload['date']
            else: event_output.name = Event.query.get(id).date
            if(ns.payload['location'] != "String"):    
                event_output.location = ns.payload['location']
            else: event_output.name = Event.query.get(id).location
            db.session.commit()
            return event_output
        else: return {'message': 'No event found'}, 404
    
    def delete(self, id):
        """Delete a single event"""
        event_output = Event.query.get(id)
        event_output.delete()
        return {'message': 'Event deleted'}, 200

#  all guests for a single event
@ns.route('/events/<int:id>/guests')
class Guests(Resource):
    @ns.marshal_list_with(guest_output_model)
    def get(self, id):
        """Get all guests for a single event"""
        guests_output = Guest.query.filter_by(event_id=id).all()  
        if guests_output:
            return guests_output
        else: return {'message': 'No guests found'}, 404
    
@ns.route('/genders')
class Genderss(Resource):
    @ns.marshal_list_with(gender_output_model)
    def get(self):
        genderr = Gender.query.all()
        if genderr:
            return genderr
        else: return "nothing found"