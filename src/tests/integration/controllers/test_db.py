import sqlite3
import pytest
from flask import Flask, g
from src.db import get_db, close_db, init_db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['DATABASE'] = ':memory:'
    app.config['TESTING'] = True

    @app.teardown_appcontext
    def teardown(exception):
        close_db()

    with app.app_context():
        init_db()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is not None
        assert isinstance(db, sqlite3.Connection)

def test_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is not None
        close_db()
        assert 'db' not in g

