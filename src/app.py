import os
import click
import sqlalchemy as sa

from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import relationship

load_dotenv()

class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlchemy's DeclarativeBase.
    """
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped["User"] = relationship(back_populates="role")
    
    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"       


class User(db.Model):
    """
    User model representing a user in the database.
    
    Attributes:
        id (int): The unique identifier for the user.
        username (str): The unique username for the user.
    """
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.
        
        Returns:
            str: A string representation of the User object.
        """
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"


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
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicialize o JWTManager com a aplicação

    from src.controllers import user, post, role, auth

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(role.app)
    app.register_blueprint(auth.app)

    return app