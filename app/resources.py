from flask_restx import Namespace, Resource
from .api_models import course_model, student_model, course_input_model, user_model, login_model
from .models import Course, Student, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

authorizations = {
    "jsonWebToken":{
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace('api', authorizations=authorizations)



@ns.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}