# SQL MCP Demo Server - Project Planning

*(Note: This document outlines the initial plan. Actual implementation details may have evolved.)*

## 1. Project Goal

To create a simple, illustrative Model Context Protocol (MCP) server using Python and the FastMCP library. This server will act as a demonstration, providing an AI agent with basic tools to interact with a PostgreSQL database containing user information.
The primary objective is to showcase a minimal but functional MCP server implementation.

## 2. Target Audience

Developers looking for a basic example of how to build an MCP server to connect custom data sources or tools to AI agents.

## 3. Core Technology Stack

*   **Language**: Python 3.10+
*   **MCP Framework**: `mcp` Python SDK
*   **Database**: PostgreSQL
*   **DB Driver**: `asyncpg`
*   **Configuration**: Environment Variables (`python-dotenv`)
*   **Dependency Management**: `uv`
*   **Deployment**: Docker

## 4. Proposed Architecture

*   **Server Entrypoint**: A single Python script (`sqlmcp/server.py`) initializing the `FastMCP` server.
*   **Database Interaction**: Encapsulate database connection and query logic within a simple dedicated class (`sqlmcp/database_management.py`). Use asynchronous connections via `asyncpg`.
*   **MCP Transport**: SSE (Server-Sent Events) for Docker deployment and Stdio for local development/debugging.
*   **Lifespan Management**: Utilize FastMCP's lifespan context manager to handle database connection setup and teardown.

## 5. Data Model

*   A single PostgreSQL table named `users`.
*   Columns:
    *   `id`: SERIAL PRIMARY KEY
    *   `name`: TEXT NOT NULL
    *   `email`: TEXT UNIQUE NOT NULL

## 6. Planned MCP Tools

The initial set of tools will provide basic CRUD operations on the `users` table:

1.  **`add_user(name: str, email: str) -> str`**: Adds a new user record.
2.  **`get_all_users() -> List[Dict]`**: Retrieves all user records.
3.  **`find_user_by_email(email: str) -> Union[Dict, str]`**: Fetches a single user by their unique email.
4.  **`delete_user_by_email(email: str) -> str`**: Removes a user record based on email.

## 7. Development Practices & Tooling

*   **Formatting**: Use `ruff format`.
*   **Linting**: Use `ruff check`.
*   **Testing Framework**: Plan to use `pytest` for unit tests (to be added later).
*   **Virtual Environments**: Managed via `python -m venv`.
*   **Dependency Installation**: Use `uv pip install`.

## 8. Deployment Strategy

*   Provide a `Dockerfile` for building a container image.
*   Include instructions for running via `docker build` and `docker run`.
*   Optionally include `docker-compose` setup if integrating with other services becomes necessary.

## 9. Future Considerations / Potential Improvements (Post-MVP)

*   **Testing**: Implement comprehensive unit tests for tools and database logic.
*   **Error Handling**: Enhance error reporting from tools (e.g., more specific error messages).
*   **Input Validation**: Use Pydantic within tool definitions for robust parameter validation.
*   **Security**: Implement optional request signing using `MCP_SIGNING_KEY`.
*   **Scalability**: Investigate more robust database connection pooling if usage increases.
*   **Advanced Queries**: Add tools for more complex searches (e.g., filtering by name patterns).
*   **Documentation**: Improve inline code comments and potentially generate API documentation.

## 10. File Structure Plan

```
agents-mcp-demo/
├── sqlmcp/
│   ├── server.py             # Main FastMCP server logic, tool definitions
│   └── database_management.py # Class for handling DB connections & queries
├── tests/                    # (Planned) Unit tests
│   └── sqlmcp/
│       └── ...
├── .env.example            # Example environment variables
├── Dockerfile                # Docker build definition
├── pyproject.toml            # Project metadata, dependencies, tool config
├── README.md                 # User guide, setup instructions
├── PLANNING.md               # Project planning
└── TASKS.md                  # Task tracking
```

## Style Guidelines
- Follow PEP8 standards
- Use type hints for all functions
- Document functions with Google-style docstrings
- Format code with Black
- Use Pydantic for data validation

## Dependencies
- mcp
- sqlalchemy