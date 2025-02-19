from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.models.user import User, db
from flask_jwt_extended import create_access_token
from http import HTTPStatus

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route('/login', methods=['POST'])
def login():
    """
    Handle user login and return a JWT access token.

    This endpoint expects a JSON payload with 'username' and 'password'.
    If the credentials are valid, it returns a JWT access token.
    Otherwise, it returns an error message with HTTP status 401.

    Returns:
        dict: A dictionary containing the access token or an error message.
        HTTPStatus: The HTTP status code.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    
    if not user or user.password != password:
        return {"error": "Invalid username or password"}, HTTPStatus.UNAUTHORIZED
    
    acess_token = create_access_token(identity=str(user.id))

    return {"access_token": acess_token}, HTTPStatus.OK