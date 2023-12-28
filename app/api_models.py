from flask_restx import fields
from .extensions import api

user_input_model = api.model("Userinput", {
    "username": fields.String,
    "password": fields.String
})

gender_output_model = api.model("GenderOutput", {
    "id": fields.Integer,
    "name": fields.String,
})
gender_input_model = api.model("GenderOutput", {
    "name": fields.String,
})

guest_output_model = api.model("GuestOutput", {
    "id": fields.Integer,
    "name": fields.String,
    "gender": fields.List(fields.Nested(gender_output_model))
})

event_output_model = api.model("EventOutput", {
    "id": fields.Integer,
    "name": fields.String,
    "date": fields.String,
    "location": fields.String,
    "guests": fields.List(fields.Nested(guest_output_model))
})

guest_input_model = api.model("GuestOutput", {
    "name": fields.String,
    "gender": fields.List(fields.Nested(gender_output_model)),
    "event_id": fields.Integer
})

event_intput_model = api.model("EventOutput", {
    "name": fields.String,
    "date": fields.String,
    "location": fields.String,
    "user_id" : fields.Integer
})
event_update_model = api.model("EventOutput", {
    "name": fields.String,
    "date": fields.String,
    "location": fields.String
})

