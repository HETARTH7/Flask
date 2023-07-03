from flask_restful import Api, Resource
from bson.objectid import ObjectId
from flask import request
from app import mongo
from app.models import User

api = Api()

class UserResource(Resource):
    def get(self):
        users = User.get_all()
        return users

    def post(self):
        user_data = request.get_json()
        user = User.from_dict(user_data)
        result = user.save()
        return result


class UserItemResource(Resource):
    def get(self, id):
        user = User.get_by_id(id)
        return user

    def put(self, id):
        user_data = request.get_json()
        user = User.from_dict(user_data)
        result = user.update(id)
        return result

    def delete(self, id):
        result = User.delete(id)
        return result

api.add_resource(UserResource, '/users')
api.add_resource(UserItemResource, '/users/<string:id>')
