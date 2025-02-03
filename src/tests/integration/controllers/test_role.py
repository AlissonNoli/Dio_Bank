import pytest
from flask import Flask, json
from src.app import create_app, db, Role


def test_create_role_success(client):
    response = client.post('/roles/', json={"name": "Admin"})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["message"] == "Role created successfully"
    assert Role.query.filter_by(name="Admin").first() is not None

def test_create_role_missing_name(client):
    response = client.post('/roles/', json={})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "name" in data["message"]

def test_create_role_invalid_data(client):
    response = client.post('/roles/', json={"name": 123})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "name" in data["message"]