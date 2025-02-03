from http import HTTPStatus
from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import User, db
from flask_jwt_extended import jwt_required
from src.utils import requires_roles
from sqlalchemy.exc import IntegrityError

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
    }, HTTPStatus.CREATED

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
@requires_roles("admin")
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
# @jwt_required()
# @requires_roles("admin")
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
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            }
        }

@app.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
@requires_roles("admin")
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

    if "username" in data:
        existing_user = db.session.execute(db.select(User).filter_by(username=data["username"])).scalar()
        if existing_user and existing_user.id != user_id:
            return {"message": "Username already exists!"}, HTTPStatus.CONFLICT

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"message": "An error occurred while updating the user."}, HTTPStatus.BAD_REQUEST

    return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            }
        }

@app.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@requires_roles("admin")
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