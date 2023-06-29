from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure the Flask application to connect to MongoDB
# Assuming your MongoDB instance is running on 'mongo' service in Docker Compose
app.config['MONGO_URI'] = 'mongodb://mongo:27017/usersdb'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        user_list.append(user)
    return jsonify(user_list)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one_or_404({'_id': id})
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
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
    user_data = request.get_json()
    user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = mongo.db.users.update_one({'_id': id}, {'$set': user})
    if result.matched_count == 0:
        return jsonify({'message': 'User not found'})
    return jsonify({'message': 'User updated'})


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.users.delete_one({'_id': id})
    if result.deleted_count == 0:
        return jsonify({'message': 'User not found'})
    return jsonify({'message': 'User deleted'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
