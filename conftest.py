import sys
import os
import pytest
from src.app import create_app, db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_blog.sqlite',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))