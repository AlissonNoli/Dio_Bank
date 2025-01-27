from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.app import Role, db
from http import HTTPStatus

app = Blueprint("role", __name__, url_prefix="/roles")


@app.route('/', methods=['POST'])
def create_role():
    """
    Create a new role.

    This endpoint allows for the creation of a new role by providing the role name in the request body.

    Request Body:
    {
        "name": "string"  # The name of the role to be created
    }

    Returns:
        dict: A message indicating the role was created successfully.
        HTTPStatus: The HTTP status code indicating the result of the operation.
    """
    data = request.json
    role = Role(name=data["name"])
    
    db.session.add(role)
    db.session.commit()
    
    return {"message": "Role created successfully"}, HTTPStatus.CREATED