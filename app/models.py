from app import mongo


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password')
        )

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

    def save(self):
        user_data = self.to_dict()
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        users = mongo.db.users.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return user_list

    @staticmethod
    def get_by_id(id):
        user = mongo.db.users.find_one_or_404({'_id': ObjectId(id)})
        user['_id'] = str(user['_id'])
        return user

    def update(self, id):
        user_data = self.to_dict()
        result = mongo.db.users.update_one(
            {'_id': ObjectId(id)}, {'$set': user_data})
        if result.matched_count == 0:
            return {'message': 'User not found'}
        return {'message': 'User updated'}

    @staticmethod
    def delete(id):
        result = mongo.db.users.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            return {'message': 'User not found'}
        return {'message': 'User deleted'}
