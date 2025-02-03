from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from src.controllers.post import app as post_bp
from src.app import db, User, Post
import pytest

@pytest.fixture
def app():
    """
    Fixture to create a Flask application instance for testing.
    
    Configures the application for testing, initializes the database,
    and sets up the JWT manager and post blueprint.
    
    Yields:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(post_bp)

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

@pytest.fixture
def access_token(app):
    """
    Fixture to create an access token for the test user.
    
    Args:
        app (Flask): The Flask application instance.
    
    Returns:
        str: The access token for the test user.
    """
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        return create_access_token(identity=str(user.id))