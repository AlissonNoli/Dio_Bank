import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager
from src.controllers.auth import app as auth_bp
from src.app import db, User

@pytest.fixture
def app():
    """
    Fixture to create a Flask application instance for testing.
    
    Configures the application for testing, initializes the database,
    and sets up the JWT manager and authentication blueprint.
    
    Yields:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'
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
    """
    Fixture to create a test client for the Flask app.
    
    Args:
        app (Flask): The Flask application instance.
    
    Returns:
        FlaskClient: The test client for the Flask app.
    """
    return app.test_client()

def test_login_success(client: FlaskClient):
    """
    Test case for successful login.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 200.
        The response contains an access token.
    """
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_username(client: FlaskClient):
    """
    Test case for login with an invalid username.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Asserts:
        The response status code is 401.
    """
    response = client.post('/auth/login', json={
        'username': 'wronguser',
        'password': 'testpassword'
    })
    assert response.status_code == 401