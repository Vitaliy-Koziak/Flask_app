from flask import jsonify, request, redirect, url_for
from flask_restful import Resource,Api
from .models import *


user_schema = UserSchema()
users_schema = UserSchema(many=True)
class UsersResourseList(Resource):
    def post(self):
        pass
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return jsonify(users)




