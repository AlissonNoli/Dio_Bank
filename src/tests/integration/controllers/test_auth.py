import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager
from src.controllers.auth import app as auth_bp
from src.app import db, User

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        user = User(username='testuser', password='testpassword', role_id=1)
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client: FlaskClient):
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_username(client: FlaskClient):
    response = client.post('/auth/login', json={
        'username': 'wronguser',
        'password': 'testpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid username or password'

def test_login_invalid_password(client: FlaskClient):
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid username or password'