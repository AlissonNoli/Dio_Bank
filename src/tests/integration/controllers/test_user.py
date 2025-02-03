import pytest
from flask import Flask
from src.app import db, create_app, User, Role
from http import HTTPStatus
from sqlalchemy import func

def test_get_user_success(client):
    """
    Test case for successfully retrieving a user.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 200 (OK).
        The response JSON matches the expected user data.
    """
    # Given
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()
    
    user = User(username='test', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()
    
    # When
    response = client.get(f'/users/{user.id}')
    
    # Then
    assert response.status_code == HTTPStatus.OK 
    assert response.json == {"id": user.id, 
                             "username": user.username, 
                             "password": user.password,
                             "role": 
                                 {"id": role.id, "name": role.name}
                             }

def test_get_user_not_found(client):
    """
    Test case for retrieving a user that does not exist.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 404 (Not Found).
    """
    # Given
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()
    
    user_id = 1
    response = client.get(f'/users/{user_id}')
    
    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_user_success(client, access_token):
    """
    Test case for successfully creating a user.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
        access_token (str): The access token for authentication.
    
    Asserts:
        The response status code is 201 (Created).
        The response message indicates success.
        The user is created in the database.
    """
    # Given
    role_id = db.session.execute(db.select(Role.id).where(Role.name == 'admin')).scalar()
    payload = {"username": "user2", "password": "user2", "role_id": role_id}
    
    # When
    response = client.post('/users/', json=payload, headers={'Authorization': f'Bearer {access_token}'}, follow_redirects=True)
    
    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_list_users(client, access_token):
    """
    Test case for listing all users.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
        access_token (str): The access token for authentication.
    
    Asserts:
        The response status code is 200 (OK).
        The response JSON matches the expected list of users.
    """
    # Given
    role = db.session.execute(db.select(Role)).scalar()
    user = db.session.execute(db.select(User).where(User.username == "test")).scalar()
    
    response = client.post('/auth/login', json={"username": user.username, "password": user.password})
    access_token = response.json['access_token']
    
    # When
    response = client.get('/users', headers={'Authorization': f'Bearer {access_token}'}, follow_redirects=True)
    
    # Then 
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id, 
                "username": user.username, 
                "password": user.password,
                "role": {
                    "id": role.id, 
                    "name": role.name
                }
            }
        ]
    }