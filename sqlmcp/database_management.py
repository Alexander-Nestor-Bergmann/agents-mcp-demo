from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from .models import Base, User


class SimpleDatabaseManager:
    """
    A demo database manager class that uses SQLAlchemy to manage a database.

    Handles asynchronous database operations for User models defined in models.py.
    This class is intended for demonstration purposes.

    Attributes:
        engine: The SQLAlchemy async engine instance.
        async_session: An async sessionmaker factory bound to the engine.
    """

    def __init__(self, db_url: str):
        """
        Initialises the SimpleDatabaseManager.

        Args:
            db_url (str): The database connection URL (e.g.,
                          'sqlite+aiosqlite:///./test.db' or
                          'postgresql+asyncpg://user:pass@host/db').
        """
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def init_models(self):
        """
        Initialises the database schema.

        Creates all tables defined in the Base metadata if they don't exist.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, name: str, email: str):
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user to add.
            email (str): The unique email address of the user to add.
        """
        async with self.async_session() as session:
            async with session.begin():
                user = User(name=name, email=email)
                session.add(user)

    async def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list[User]: A list of all User objects in the database.
        """
        async with self.async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def find_user_by_email(self, email: str):
        """
        Finds a single user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            User | None: The found User object, or None if no user is found.
        """
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    async def delete_user_by_email(self, email: str):
        """
        Deletes a user from the database based on their email address.

        Args:
            email (str): The email address of the user to delete.

        Returns:
            str: A message indicating success or if the user was not found.
        """
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.email == email))
                user = result.scalar_one_or_none()
                if user:
                    await session.delete(user)
                    return f"User {email} deleted successfully."
                else:
                    return "error: User not found."

    async def close(self):
        """
        Closes the database connection engine.

        Should be called on application shutdown to release resources.
        """
        await self.engine.dispose()
