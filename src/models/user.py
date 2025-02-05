import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import db

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
    role: Mapped["role.Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.
        
        Returns:
            str: A string representation of the User object.
        """
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"