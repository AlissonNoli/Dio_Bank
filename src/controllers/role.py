from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.models import Role, db
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

    if not data or "name" not in data:
        return {"message": "Missing 'name' in request body"}, HTTPStatus.BAD_REQUEST

    if not isinstance(data["name"], str):
        return {"message": "'name' must be a string"}, HTTPStatus.BAD_REQUEST

    role = Role(name=data["name"])
    
    db.session.add(role)
    db.session.commit()
    
    return {"message": "Role created successfully"}, HTTPStatus.CREATED

@app.route('/', methods=['GET'])
def list_roles():
    """
    List all roles.

    This endpoint retrieves all roles from the database and returns them as a list of dictionaries.

    Returns:
        list: A list of dictionaries, each representing a role.
        HTTPStatus: The HTTP status code indicating the result of the operation.
    """
    roles = db.session.execute(db.select(Role)).scalars().all()
    return jsonify([
        {
            "id": role.id,
            "name": role.name
        }
        for role in roles
    ]), HTTPStatus.OK

@app.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """
    Delete a role by ID.

    This endpoint deletes a role from the database using the provided role ID.

    Args:
        role_id (int): The ID of the role to delete.

    Returns:
        dict: A message indicating the role was deleted successfully.
        HTTPStatus: The HTTP status code indicating the result of the operation.
    """
    role = db.get_or_404(Role, role_id)
    
    db.session.delete(role)
    db.session.commit()
    
    return {"message": "Role deleted successfully"}, HTTPStatus.OK