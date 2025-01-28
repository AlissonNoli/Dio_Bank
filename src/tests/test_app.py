import pytest
from flask import Flask
from src.app import db, Role, User

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_role(app):
    with app.app_context():
        role = Role(name="Admin")
        db.session.add(role)
        db.session.commit()
        assert role.id is not None
        assert role.name == "Admin"

def test_create_user(app):
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