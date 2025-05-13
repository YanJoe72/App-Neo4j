from flask import Blueprint, jsonify, request
from models import *

comment_routes = Blueprint('comment_routes', __name__)


@comment_routes.route('/posts/<post_id>/comments', methods=['GET'])
def get_comments_by_post(post_id):
    comments = get_comments_by_post_from_db(post_id)
    return jsonify(comments), 200


@comment_routes.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    content = data.get("content")
    user_id = data.get("user_id")

    if not content or not user_id:
        return jsonify({"error": "Content and user_id are required"}), 400

    comment = create_comment_in_db(post_id, user_id, content)
    return jsonify({"message": "Comment added!", "comment": comment}), 201


@comment_routes.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    if delete_comment_from_db(post_id, comment_id):
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"error": "Comment not found"}), 404


@comment_routes.route('/comments', methods=['GET'])
def get_all_comments():
    comments = get_all_comments_from_db()
    return jsonify(comments), 200


@comment_routes.route('/comments/<comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    comment = get_comment_by_id_from_db(comment_id)
    if comment:
        return jsonify(comment), 200
    return jsonify({"error": "Comment not found"}), 404


@comment_routes.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()
    new_content = data.get("content")
    comment = update_comment_in_db(comment_id, new_content)
    if comment:
        return jsonify(comment), 200
    return jsonify({"error": "Comment not found"}), 404


@comment_routes.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment_by_id(comment_id):
    if delete_comment_by_id_from_db(comment_id):
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"error": "Comment not found"}), 404


@comment_routes.route('/comments/<comment_id>/like', methods=['POST'])
def add_like_to_comment(comment_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if add_like_to_comment_in_db(user_id, comment_id):
        return jsonify({"message": "Like added"}), 200
    return jsonify({"error": "User or comment not found"}), 404


@comment_routes.route('/comments/<comment_id>/like', methods=['DELETE'])
def remove_like_from_comment(comment_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if remove_like_from_comment_in_db(user_id, comment_id):
        return jsonify({"message": "Like removed"}), 200
    return jsonify({"error": "Like not found"}), 404