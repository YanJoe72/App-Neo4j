from flask import Blueprint, jsonify, request
from models import *

post_routes = Blueprint('post_routes', __name__)

@post_routes.route('/posts', methods=['GET'])
def get_all_posts():
    posts = get_all_posts_from_db()
    return jsonify(posts), 200

@post_routes.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    post = get_post_by_id_from_db(post_id)  # Fonction à implémenter
    if post:
        return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404

@post_routes.route('/users/<user_id>/posts', methods=['GET'])
def get_user_posts_route(user_id):
    posts = get_posts_by_user(user_id)
    return jsonify(posts), 200

@post_routes.route('/users/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "Content is required"}), 400

    post = create_post_in_db(user_id, content)  # Fonction à implémenter
    return jsonify({"message": "Post created!", "post": post}), 201

@post_routes.route('/posts/<post_id>', methods=['PUT'])
def update_post_route(post_id):
    data = request.get_json()
    new_content = data.get("content")
    post = update_post(post_id, new_content)
    if post:
        return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404

@post_routes.route('/posts/<post_id>', methods=['DELETE'])
def delete_post_route(post_id):
    if delete_post(post_id):
        return jsonify({"message": "Post deleted successfully"}), 200
    return jsonify({"error": "Post not found"}), 404

@post_routes.route('/posts/<post_id>/like', methods=['POST'])
def add_like_route(post_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if add_like_to_post(user_id, post_id):
        return jsonify({"message": "Like added"}), 200
    return jsonify({"error": "User or post not found"}), 404

@post_routes.route('/posts/<post_id>/like', methods=['DELETE'])
def remove_like_route(post_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if remove_like_from_post(user_id, post_id):
        return jsonify({"message": "Like removed"}), 200
    return jsonify({"error": "Like not found"}), 404