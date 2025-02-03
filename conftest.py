import sys
import os
import pytest
from src.app import create_app, db, User, Role

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

@pytest.fixture()
def app():
    """
    Fixture to create a Flask application instance for testing.
    
    Configures the application for testing, initializes the in-memory database,
    and sets up the teardown context to close the database after each test.
    
    Yields:
        Flask: The Flask application instance.
    """
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        
@pytest.fixture()
def client(app):
    """
    Fixture to create a test client for the Flask app.
    
    Args:
        app (Flask): The Flask application instance.
    
    Returns:
        FlaskClient: The test client for the Flask app.
    """
    return app.test_client()

@pytest.fixture()
def access_token(client):
    """
    Fixture to create an access token for the test user.
    
    Args:
        client (FlaskClient): The test client for the Flask app.
    
    Returns:
        str: The access token for the test user.
    """
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()
    
    user = User(username='test', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()
    
    response = client.post('/auth/login', json={"username": user.username, "password": user.password})
    return response.json['access_token']
