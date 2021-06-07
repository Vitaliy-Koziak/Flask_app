from flask import request
from flask_restful import Resource
from .models import *


users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UsersResourceList(Resource):
    def post(self):
        user_json = request.json
        if not user_json:
            return {'message': "Wrong date"}, 400
        try:
            user = User(
                email = user_json['email'],
                first_name = user_json['first_name'],
                date = user_json['date'],
                salary = user_json.get('salary'),
                department_id = user_json.get('department_id')
            )
            db.session.add(user)
            db.session.commit()

        except(ValueError, KeyError):
            return {'message': 'Wrong date'}, 400
        return {'message': "created successfully"}, 201

    def get(self, id=None):
        if not id:
            users = db.session.query(User).all()
            users = users_schema.dump(users)
            return users, 200
        user = db.session.query(User).filter_by(id=id).first()
        user = user_schema.dump(user)

        if not user:
            return 'not one yet', 404
        return user, 200
