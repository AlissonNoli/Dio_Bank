import os
import click
import sqlalchemy as sa

from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlchemy's DeclarativeBase.
    """
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    """
    User model representing a user in the database.
    
    Attributes:
        id (int): The unique identifier for the user.
        username (str): The unique username for the user.
    """
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    # email: Mapped[str] = mapped_column(sa.String)

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.
        
        Returns:
            str: A string representation of the User object.
        """
        return f"User(id={self.id!r}, username={self.username!r})"


class Post(db.Model):
    """
    Post model representing a blog post in the database.
    
    Attributes:
        id (int): The unique identifier for the post.
        title (str): The title of the post.
        body (str): The body content of the post.
        created (datetime): The timestamp when the post was created.
        author_id (int): The ID of the user who authored the post.
    """
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        """
        Return a string representation of the Post object.
        
        Returns:
            str: A string representation of the Post object.
        """
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"


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
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.cli.add_command(init_db_command)

    db.init_app(app)

    from src.controllers import user, post

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)

    return app