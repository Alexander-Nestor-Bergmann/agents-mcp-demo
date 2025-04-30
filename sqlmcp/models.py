from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for SQLAlchemy models with async support."""

    pass


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): Primary key identifier for the user.
        name (str): The user's name.
        email (str): The user's unique email address.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
