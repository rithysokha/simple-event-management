from flask import Flask
from .extensions import api, db, jwt
from .resources import ns, uns
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["JWT_SECRET_KEY"] = "secretkey"
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.add_namespace(ns)
    api.add_namespace(uns)
    return app