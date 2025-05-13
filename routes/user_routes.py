from flask import Blueprint, jsonify, request
from models import *

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users)

@user_routes.route('/users', methods=['POST'])
def create_new_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    user = create_user(name, email)
    return jsonify({"message": "User created successfully!", "user": user["id"]}), 201

@user_routes.route('/users/<user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@user_routes.route('/users/<user_id>', methods=['PUT'])
def update_user_by_id_route(user_id):
    data = request.get_json()
    user = get_user_by_id(user_id)
    user.name = data.get('name')
    user.email = data.get('email')
    if user:
        return jsonify({"error": "User already exist"}), 400
    return jsonify(user)

@user_routes.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": "User deleted successfully!"})
    return jsonify({"error": "User not found"}), 404

@user_routes.route("/users/<user_id>/friends", methods=["GET"])
def get_user_friends(user_id):
    friends = get_friends(user_id)
    return jsonify(friends)

@user_routes.route('/users/<user_id>/friends', methods=['POST'])
def add_friend_route(user_id):
    data = request.get_json()
    friend_id = data.get('friend_id')
    if not friend_id:
        return jsonify({"error": "Friend ID is required"}), 400
    result = add_friend(user_id, friend_id)
    return jsonify(result)

@user_routes.route('/users/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend_route(user_id, friend_id):
    if remove_friend(user_id, friend_id):
        return jsonify({"message": "Friendship removed successfully"}), 200
    return jsonify({"error": "Friendship not found"}), 404

@user_routes.route('/users/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship_route(user_id, friend_id):
    if are_friends(user_id, friend_id):
        return jsonify({"friends": True}), 200
    return jsonify({"friends": False}), 200

@user_routes.route('/users/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def mutual_friends_route(user_id, other_id):
    mutual_friends = get_mutual_friends(user_id, other_id)
    return jsonify(mutual_friends), 200