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

@ns.route('/course')
class CourseListApi(Resource):
    method_decorators = [jwt_required()]
    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(course_model)
    @ns.marshal_with(course_model)
    def get(self):
        
        return Course.query.all()
    @ns.expect(course_input_model)
    def post(self):
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course

@ns.route('/course/<int:id>')
class CourseApi(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        return Course.query.get(id)
    
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course
    
    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return '', 204

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course
    
@ns.route('/student')
class StudentApi(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

@ns.route('/register')
    class Register(Resource):
        @ns.expect(login_model)
        @ns.marshal_with(user_model)
        def post(self):
            