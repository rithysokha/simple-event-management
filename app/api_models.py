from flask_restx import fields
from .extensions import api

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    # "students": fields.List(fields.Nested(student_model))  
})

student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    "courses": fields.Nested(course_model)
    })

course_input_model = api.model("CourseInput", {
    "name": fields.String(required=True)
    })

login_model = api.model("Login", {
    "username": fields.String,
    "password": fields.String
})
user_model = api.model("User", {
    "id": fields.Integer,
    "username": fields.String
})