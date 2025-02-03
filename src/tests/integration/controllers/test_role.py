import pytest
from flask import Flask, json
from src.app import create_app, db, Role

def test_create_role_success(client):
    """
    Test case for successfully creating a role.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 201.
        The response message indicates success.
        The role "Admin" is created in the database.
    """
    response = client.post('/roles/', json={"name": "Admin"})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["message"] == "Role created successfully"
    assert Role.query.filter_by(name="Admin").first() is not None

def test_create_role_missing_name(client):
    """
    Test case for creating a role with missing name.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 400.
        The response message indicates the missing name.
    """
    response = client.post('/roles/', json={})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "name" in data["message"]

def test_create_role_invalid_data(client):
    """
    Test case for creating a role with invalid data.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 400.
        The response message indicates the invalid data.
    """
    response = client.post('/roles/', json={"name": 123})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "name" in data["message"]