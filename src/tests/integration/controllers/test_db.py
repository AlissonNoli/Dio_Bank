import sqlite3
import pytest
from flask import Flask, g
from src.db import get_db, close_db, init_db

@pytest.fixture
def app():
    """
    Fixture to create a Flask application instance for testing.
    
    Configures the application for testing, initializes the in-memory database,
    and sets up the teardown context to close the database after each test.
    
    Yields:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)
    app.config['DATABASE'] = ':memory:'
    app.config['TESTING'] = True

    @app.teardown_appcontext
    def teardown(exception):
        """
        Teardown function to close the database after each test.
        
        Args:
            exception (Exception): The exception that caused the teardown, if any.
        """
        close_db()

    with app.app_context():
        init_db()

    return app