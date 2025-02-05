import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.models.base import db

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