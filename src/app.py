import os
import click
import sqlalchemy as sa

from flask import Flask, current_app
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.db import init_db_command
from src.models import db

load_dotenv()

migrate = Migrate()
jwt = JWTManager()

@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.
    
    This command initializes the database by creating all the tables defined in the models.
    It should be registered as a CLI command for the Flask application.
    """
    global db
    try:
        with current_app.app_context():
            db.create_all()
        click.echo('Initialized the database.')
    except Exception as e:
        click.echo(f"Error initializing the database: {e}")


def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): A dictionary containing configuration settings for testing.
    
    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///blog.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        if 'TESTING' in test_config and test_config['TESTING']:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    app.cli.add_command(init_db_command)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from src.controllers import user, post, role, auth

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(role.app)
    app.register_blueprint(auth.app)

    return app