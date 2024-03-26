from flask import Flask
from .extensions import api,db
from .resources import *

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(nd)
    api.add_namespace(ndoc)

    return app

#db.create_all()