import sys
import os

# Add project root to sys.path so `from src.` imports work
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

"""Main entry point for the Postgres Events MCP server using FastMCP."""

import asyncio
from datetime import datetime
import json
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

from sqlmcp.database_management import SimpleDatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


load_dotenv()


@dataclass
class SqlDatabaseContext:
    """Context holding the database connection pool."""

    db: SimpleDatabaseManager | None = None


@asynccontextmanager
async def db_lifespan(server: FastMCP) -> AsyncIterator[SqlDatabaseContext]:
    """
    Manages the lifecycle of the SimpleDatabaseManager instance.

    Args:
        server (FastMCP): The FastMCP server instance.

    Yields:
        SqlDatabaseContext: The context containing the connection pool.

    Raises:
        ValueError: If the DB_URL environment variable is not set.
        Exception: Propagates database connection errors.
    """

    db = None
    try:
        logger.info("Attempting to connect to PostgreSQL database...")

        DB_URL = os.getenv("DB_URL")
        if not DB_URL:
            raise ValueError("DB_URL environment variable is not set.")

        db = SimpleDatabaseManager(db_url=DB_URL)
        # Ensure database tables are created
        await db.init_models()
        logger.info("Database connection pool initialized successfully.")
        yield SqlDatabaseContext(db=db)
    except Exception as e:
        logger.error(f"Failed to connect to or initialize database: {e}", exc_info=True)
        raise e
    finally:
        if db:
            logger.info("Closing database connection pool.")
            await db.close()
        else:
            logger.warning("No active database connection pool to close.")


# Initialize FastMCP server
mcp = FastMCP(
    "sql-mcp-demo",
    description="""Access a PostgreSQL database to manage user records.
    Provides tools to add, retrieve, find, and delete users.
    The 'users' table has the following structure:
        id (int): Unique identifier for the user.
        name (str): The name of the user.
        email (str): The email of the user (unique).
    """,
    lifespan=db_lifespan,
    host=os.getenv("DB_HOST", "0.0.0.0"),
    port=int(os.getenv("DB_PORT", 8051)),
)


@mcp.tool()
async def add_user(ctx: Context, name: str, email: str) -> str:
    """
    Adds a new user to the 'users' table.

    Args:
        ctx (Context): The MCP context containing request details.
        name (str): The name of the user to add.
        email (str): The unique email address of the user to add.

    Returns:
        str: A success message or an error string starting with "error:".
    """
    logger.info(f"Received add_user request: Name='{name}', Email='{email}'")

    db = ctx.request_context.lifespan_context.db
    if not db:
        logger.error("Database not available for add_user.")
        return "error: Database connection not available."

    try:
        await db.add_user(name=name, email=email)
        logger.info(f"User {name} ({email}) added successfully.")
        return f"User '{name}' added successfully."
    except Exception as e:
        logger.error(f"Failed to add user {name} ({email}): {e}", exc_info=True)
        return f"error: Failed to add user. Reason: {e}"


@mcp.tool()
async def get_all_users(ctx: Context) -> list[dict[str, Any]] | str:
    """
    Retrieves all users from the 'users' table.

    Args:
        ctx (Context): The MCP context.

    Returns:
        Union[List[Dict[str, Any]], str]: A list of user dictionaries
        (each containing 'id', 'name', 'email') or an error string.
    """
    logger.info("Received get_all_users request.")

    db = ctx.request_context.lifespan_context.db
    if not db:
        logger.error("Database not available for get_all_users.")
        return "error: Database connection not available."

    try:
        users = await db.get_all_users()
        # Convert each User object to a dictionary
        user_list = [
            {"id": user.id, "name": user.name, "email": user.email} for user in users
        ]
        logger.info(f"Retrieved {len(user_list)} users.")
        return user_list
    except Exception as e:
        logger.error(f"Failed to get all users: {e}", exc_info=True)
        return "error: Failed to retrieve users from the database."


@mcp.tool()
async def find_user_by_email(ctx: Context, email: str) -> dict[str, Any] | str:
    """
    Finds a user by their email address in the 'users' table.

    Args:
        ctx (Context): The MCP context.
        email (str): The email address to search for.

    Returns:
        Union[Dict[str, Any], str]: The user dictionary if found,
        "error: User not found." if not found, or another error string
        if a database issue occurs.
    """
    logger.info(f"Received find_user_by_email request: Email='{email}'")

    db = ctx.request_context.lifespan_context.db
    if not db:
        logger.error("Database not available for find_user_by_email.")
        return "error: Database connection not available."

    try:
        user = await db.find_user_by_email(email=email)
        if user:
            logger.info(f"User found for email: {email}")
            # Convert the User object to a dictionary explicitly
            return {"id": user.id, "name": user.name, "email": user.email}
        else:
            logger.warning(f"User not found for email: {email}")
            return "error: User not found."
    except Exception as e:
        logger.error(f"Failed to find user by email {email}: {e}", exc_info=True)
        return "error: Failed to query user from the database."


@mcp.tool()
async def delete_user_by_email(ctx: Context, email: str) -> str:
    """
    Deletes a user by their email address from the 'users' table.

    Args:
        ctx (Context): The MCP context.
        email (str): The email address of the user to delete.

    Returns:
        str: A success message if deletion was successful or indicates user
             not found, or an error string if a database issue occurs.
    """
    logger.info(f"Received delete_user_by_email request: Email='{email}'")

    db = ctx.request_context.lifespan_context.db
    if not db:
        logger.error("Database not available for delete_user_by_email.")
        return "error: Database connection not available."

    try:
        # db.delete_user_by_email returns a specific string on success/failure
        result_message = await db.delete_user_by_email(email=email)

        # Check the content of the message returned by the db manager
        if result_message.startswith("error:"):
            logger.warning(
                f"Delete operation reported issue for email {email}: {result_message}"
            )
            # Pass the specific error message (e.g., "error: User not found.") back
            return result_message
        else:
            logger.info(
                f"User with email {email} deleted successfully (reported by DB manager)."
            )
            # Return the success message from the db manager
            return result_message

    except Exception as e:
        logger.error(f"Failed to delete user by email {email}: {e}", exc_info=True)
        return (
            "error: Failed to delete user from the database due to an unexpected error."
        )


async def main():
    """Starts the MCP server."""
    transport = os.getenv("TRANSPORT", "sse")
    logger.info(f"Starting Postgres MCP server using {transport} transport.")
    if transport == "sse":
        await mcp.run_sse_async()
    elif transport == "stdio":
        await mcp.run_stdio_async()
    else:
        logger.error(f"Unsupported transport type: {transport}. Use 'sse' or 'stdio'.")


if __name__ == "__main__":
    asyncio.run(main())
