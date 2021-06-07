from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
from . import db
app = Flask(__name__)
ma = Marshmallow(app)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,unique=True)
    email = db.Column(db.String(40),unique=True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(150))
    date = db.Column(db.String(10))
    salary = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship("Department")
    def __repr__(self):
        return f"{self.id} {self.first_name} {self.email} {self.date} {self.department}"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return self.name



class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("email", "first_name","date","department_id","salary")
    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )

