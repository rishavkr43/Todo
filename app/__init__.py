from flask import Flask
from  flask_sqlalchemy import SQLAlchemy

#create database object globally

db= SQLAlchemy()

# creating flask app instance
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] ='tech-to-evolve'
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] =False

    db.__init__(app)
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)  
    app.register_blueprint(tasks_bp)    

    with app.app_context():
        db.create_all()

    return app
