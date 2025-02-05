from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Post
from http import HTTPStatus
from sqlalchemy import inspect


app = Blueprint("post", __name__, url_prefix="/posts")


@app.route('/', methods=['POST'])
@jwt_required()
def _create_post():
    """
    Create a new post and add it to the database.
    
    This function retrieves the JSON data from the request, creates a new Post object,
    adds it to the database session, and commits the session.
    
    Returns:
        dict: A dictionary containing the ID, title, body, created, and author_id of the newly created post.
    """
    user_id = get_jwt_identity()
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }), HTTPStatus.CREATED


def _list_posts():
    """
    Retrieve a list of all posts from the database.
    
    This function executes a SELECT query on the Post table and returns a list of dictionaries,
    each containing the ID, title, body, created, and author_id of a post.
    
    Returns:
        list: A list of dictionaries, each representing a post.
    """
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id,
        }
        for post in posts
    ]


@app.route('/', methods=['GET', 'POST'])
def list_or_create_post():
    """
    Handle requests to list all posts or create a new post.
    
    If the request method is POST, a new post is created using the _create_post function.
    If the request method is GET, a list of all posts is returned using the _list_posts function.
    
    Returns:
        dict: A dictionary containing a message if a new post is created, or a list of posts.
        int: The HTTP status code.
    """
    if request.method == 'POST':
        post = _create_post()
        return jsonify(post), HTTPStatus.CREATED
    else:
        posts = _list_posts()
        return jsonify({"posts": posts}), HTTPStatus.OK


@app.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Retrieve the details of a specific post by post ID.
    
    This function retrieves a post from the database using the post ID and returns a dictionary
    containing the post's ID, title, body, created, and author_id.
    
    Args:
        post_id (int): The ID of the post to retrieve.
    
    Returns:
        dict: A dictionary containing the ID, title, body, created, and author_id of the post.
    """
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@app.route('/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    """
    Update the details of a specific post by post ID.
    
    This function retrieves a post from the database using the post ID, updates the post's attributes
    with the provided JSON data, and commits the changes to the database.
    
    Args:
        post_id (int): The ID of the post to update.
    
    Returns:
        dict: A dictionary containing the updated ID, title, body, created, and author_id of the post.
    """
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@app.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a specific post by post ID.
    
    This function retrieves a post from the database using the post ID, deletes the post,
    and commits the changes to the database.
    
    Args:
        post_id (int): The ID of the post to delete.
    
    Returns:
        str: An empty string.
        int: The HTTP status code indicating no content.
    """
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT