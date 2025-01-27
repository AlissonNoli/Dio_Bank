from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.app import User, db
from http import HTTPStatus
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    """
    Create a new user and add it to the database.
    
    This function retrieves the JSON data from the request, creates a new User object,
    adds it to the database session, and commits the session.
    
    Returns:
        dict: A dictionary containing the ID and username of the newly created user.
    """
    data = request.json
    
    user = User(
        username=data["username"],
        password=data["password"],  
        role_id=data["role_id"],  
    )
    
    db.session.add(user)
    db.session.commit()
    return {
        "id": user.id,
        "username": user.username,
    }

def _list_users():
    """
    Retrieve a list of all users from the database.
    
    This function executes a SELECT query on the User table and returns a list of dictionaries,
    each containing the ID and username of a user.
    
    Returns:
        list: A list of dictionaries, each representing a user.
    """
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            }
        }
        for user in users
    ]

@app.route('/', methods=['GET', 'POST'])
@jwt_required()
def list_or_create_user():
    """
    Handle requests to list all users or create a new user.
    
    If the request method is POST, a new user is created using the _create_user function.
    If the request method is GET, a list of all users is returned using the _list_users function.
    
    Returns:
        dict: A dictionary containing a message if a new user is created, or a list of users.
        int: The HTTP status code.
    """
    if request.method == 'POST':
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}, HTTPStatus.OK

@app.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve the details of a specific user by user ID.
    
    This function retrieves a user from the database using the user ID and returns a dictionary
    containing the user's ID and username.
    
    Args:
        user_id (int): The ID of the user to retrieve.
    
    Returns:
        dict: A dictionary containing the ID and username of the user.
    """
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    """
    Update the details of a specific user by user ID.
    
    This function retrieves a user from the database using the user ID, updates the user's attributes
    with the provided JSON data, and commits the changes to the database.
    
    Args:
        user_id (int): The ID of the user to update.
    
    Returns:
        dict: A dictionary containing the updated ID and username of the user.
    """
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a specific user by user ID.
    
    This function retrieves a user from the database using the user ID, deletes the user,
    and commits the changes to the database.
    
    Args:
        user_id (int): The ID of the user to delete.
    
    Returns:
        str: An empty string.
        int: The HTTP status code indicating no content.
    """
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT