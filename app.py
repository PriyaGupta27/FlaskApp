from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

connection_uri = "mongodb://localhost:27017/Info"
client = MongoClient(connection_uri)

db = client['Info']
collection = db['Info']

user_fields = {'name': True, 'email': True, 'password': True}

@app.route('/users', methods=['GET'])
def get_users():
    users = collection.find({}, user_fields)
    user_list = [user for user in users]
    return jsonify({'users': user_list})

@app.route('/users/<string:id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({'_id': id}, user_fields)
    if user:
        return jsonify({'user': user})
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' in data and 'email' in data and 'password' in data:
        user_id = collection.insert(data)
        new_user = collection.find_one({'_id': user_id}, user_fields)
        return jsonify({'user': new_user}), 201
    return jsonify({'message': 'Incomplete user data'}), 400

@app.route('/users/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if 'name' in data or 'email' in data or 'password' in data:
        collection.update({'_id': id}, {'$set': data})
        updated_user = collection.find_one({'_id': id}, user_fields)
        return jsonify({'user': updated_user})
    return jsonify({'message': 'No fields to update'}), 400

@app.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': id})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
