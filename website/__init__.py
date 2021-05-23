from flask import Flask, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path
from flask_login import LoginManager
from flask_restful import Resource, Api
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
DB_NAME = "database.db"
#engine = create_engine('sqlite:///database.db')
#session = scoped_session(sessionmaker(autocommit = False,autoflush = False,bind = engine))
#Base = declarative_base()
#Base.query = session.query_property()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vitaliy'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    api = Api(app)



    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    from website.rest import UsersResourseList
    api.add_resource(UsersResourseList,"/users","/users/<int:id>")

    from website.models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app




def create_database(app):
    if not path.exists('Flask_app/'+DB_NAME):
        db.create_all(app=app)



