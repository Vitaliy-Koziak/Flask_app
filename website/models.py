from flask import Flask

from .import db
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40),unique=True)
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(150))
    date = db.Column(db.String(20))
    department = db.Column(db.String(50))
    salary = db.Column(db.Integer)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("email", "first_name","date","department","salary")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )