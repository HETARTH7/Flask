from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongo:27017/flaskdb'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return jsonify(user_list)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one_or_404({'_id': ObjectId(id)})
    user['_id'] = str(user['_id'])
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = mongo.db.users.insert_one(user)
    return jsonify(str(result.inserted_id))


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    if request.method == 'PUT':
        user_data = request.get_json()
        user = {
            'name': user_data['name'],
            'email': user_data['email'],
            'password': user_data['password']
        }
        result = mongo.db.users.update_one(
            {'_id': ObjectId(id)}, {'$set': user})
        if result.matched_count == 0:
            return jsonify({'message': 'User not found'})
        return jsonify({'message': 'User updated'})


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    if request.method == 'DELETE':
        result = mongo.db.users.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({'message': 'User not found'})
        return jsonify({'message': 'User deleted'})


if __name__ == '__main__':
    app.run(debug=True)
