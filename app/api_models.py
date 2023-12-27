from flask_restx import fields
from .extensions import api

guest_output_model = api.model("GuestOutput", {
    "id": fields.Integer,
    "name": fields.String,
    "gender": fields.String
})

event_output_model = api.model("EventOutput", {
    "id": fields.Integer,
    "name": fields.String,
    "date": fields.DateTime,
    "location": fields.String,
    "guests": fields.List(fields.Nested(guest_output_model))
})

guest_input_model = api.model("GuestOutput", {
    "name": fields.String,
    "gender": fields.String
})

event_intput_model = api.model("EventOutput", {
    "name": fields.String,
    "date": fields.DateTime,
    "location": fields.String,
    "guests": fields.List(fields.Nested(guest_input_model))
})