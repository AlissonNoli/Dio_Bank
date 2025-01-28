import pytest
from flask import Flask, json
from src.app import create_app, db, Role

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

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