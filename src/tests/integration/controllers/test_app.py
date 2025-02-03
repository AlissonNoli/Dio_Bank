import pytest
from flask import Flask
from src.app import db, Role, User

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

def test_create_role(app):
    """
    Test case to create a new role in the database.
    
    Args:
        app (Flask): The Flask application instance.
    
    Asserts:
        The role ID is not None.
        The role name is "Admin".
    """
    with app.app_context():
        role = Role(name="Admin")
        db.session.add(role)
        db.session.commit()
        assert role.id is not None
        assert role.name == "Admin"

def test_create_user(app):
    """
    Test case to create a new user in the database.
    
    Args:
        app (Flask): The Flask application instance.
    
    Asserts:
        The user ID is not None.
        The username is "testuser".
        The user's role is the created role.
    """
    with app.app_context():
        role = Role(name="User")
        db.session.add(role)
        db.session.commit()
        
        user = User(username="testuser", password="password", active=True, role=role)
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        assert user.username == "testuser"
        assert user.role == role