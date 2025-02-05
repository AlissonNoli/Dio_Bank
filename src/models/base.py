from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlchemy's DeclarativeBase.
    """
    pass

db = SQLAlchemy(model_class=Base)