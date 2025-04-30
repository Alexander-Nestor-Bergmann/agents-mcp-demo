# A Template MCP Server

This repository serves as a template, demonstrating how to implement an MCP ([Model Context Protocol](https://modelcontextprotocol.io)) server - an open standard designed to connect AI agents and services (like Claude) to tools and data sources. **The primary goal of this repository is to illustrate how to build, configure, and run a basic MCP server.** The tools are simplified examples and not intended for production use.

This specific example server uses a simple PostgreSQL database backend to manage user data, showcasing how MCP can bridge the gap between AI agents and external resources.

## Overview

The server acts as a secure gateway between an MCP client (e.g., an AI agent) and an external data source (in this case, a toy PostgreSQL database containing a `users` table). It demonstrates how to:

*   Define and expose custom tools via the MCP standard.
*   Handle requests from an MCP client.
*   Translate those requests into operations on the backend resource (e.g., database queries).
*   Return structured results or errors back to the client.

The demo `users` table used in this example has the following structure:
*   `id` (integer, primary key)
*   `name` (text)
*   `email` (text, unique)

## Example Tools Exposed by the Server

To illustrate how tools are defined and exposed, this server implements the following example functions for interacting with the user database:

*   **`add_user`**: Adds a new user to the database.
    *   *Parameters*: `name` (string), `email` (string)
    *   *Returns*: Confirmation message (string) or error.
*   **`get_all_users`**: Retrieves a list of all users from the database.
    *   *Parameters*: None
    *   *Returns*: List of user objects (each a dictionary with `id`, `name`, `email`) or error.
*   **`find_user_by_email`**: Finds a specific user by their email address.
    *   *Parameters*: `email` (string)
    *   *Returns*: A single user object (dictionary) or an error if not found.
*   **`delete_user_by_email`**: Deletes a user from the database based on their email address.
    *   *Parameters*: `email` (string)
    *   *Returns*: Confirmation message (string) or error.

These tools serve as concrete examples of the kinds of operations an MCP server might provide access to.

## Prerequisites

*   Python 3.10+
*   Access to a PostgreSQL database. The server needs connection details.
*   Docker (recommended for running the server easily).
*   `uv` (for local development dependency management).

## Configuration

Environment variables are used to configure the database connection and server settings. Copy the `.env.example` file to `.env` and update the values:

```bash
cp .env.example .env
# Edit .env with your database details and desired server settings
```

Key variables:

| Variable          | Description                                                                 | Example                                            | Required | Default   |
| ----------------- | --------------------------------------------------------------------------- | -------------------------------------------------- | :------: | --------- |
| `DB_URL`          | Full PostgreSQL connection URL.                                             | `postgresql+asyncpg://user:pass@host:5432/dbname`  |   Yes    |           |
| `DB_HOST`         | Host address for the MCP server to listen on.                               | `0.0.0.0`                                          |    No    | `0.0.0.0` |
| `DB_PORT`         | Port for the MCP server to listen on.                                       | `8051`                                             |    No    | `8051`    |                                        |    No    | `INFO`    |
| `MCP_SIGNING_KEY` | Optional secret key for signing requests between client and server.         | `your_very_secret_key`                           |    No    |           |

**Note:** The `DB_URL` should use an asyncpg compatible driver prefix like `postgresql+asyncpg://`.

## Usage

### Using Docker (Recommended)

1.  **Build the Image**:
    *(Ensure you have Docker installed and running)*
    ```bash
    # Navigate to the project root directory (agents-mcp-demo)
    docker build -t sql-mcp-demo-server --build-arg PORT=${DB_PORT:-8051} .
    ```

2.  **Run the Container**:
    ```bash
    docker run --rm -d --env-file .env -p ${DB_PORT:-8051}:${DB_PORT:-8051} --name sql-mcp-server sql-mcp-demo-server
    ```

### Local Development

1.  **Install Dependencies**: Requires `uv`. Navigate to the project root directory.
    ```bash
    # Create a virtual environment (recommended)
    python -m venv .venv
    source .venv/bin/activate # or .\.venv\Scripts\activate on Windows
    # Install using uv
    uv pip install -e .[dev]
    ```
2.  **Set Environment Variables**: Ensure the required `DB_URL` is set in your shell environment or is present in a `.env` file in the root directory (dotenv is used).
3.  **Run the Server**:
    ```bash
    uv run python sqlmcp/server.py
    ```
    *(The server will use host/port from environment variables or defaults)*

### Connecting with an MCP Client

Configure your MCP client to connect to the running server. The connection details depend on how you are running the server.

**Example SSE Configuration (if running via Docker/Compose):**

```json
{
  "mcpServers": {
    "sqlDemoServer": { // Choose a name for this server connection
      "transport": "sse",
      "url": "http://localhost:8051/sse", // Adjust port if changed from default
    }
  }
}
```

**Example Stdio Configuration (for local development):**

This allows the client to directly manage the server process.

```json
{
  "mcpServers": {
    "sqlDemoServerLocal": { // Choose a name
      "command": "python", // Or path to python in your venv e.g., ".venv/bin/python"
      "args": ["sqlmcp/server.py"], // Path relative to workspace root
      "env": {
        "TRANSPORT": "stdio", // Crucial: Tells server to use stdio
        "DB_URL": "postgresql+asyncpg://user:pass@host:5432/dbname", // MUST provide DB URL
      },
      "workingDirectory": "." // Ensure paths are resolved correctly
    }
  }
}
```

*(Adjust paths, URLs, ports, and connection details based on your specific setup.)*

## Development Practices

*   **Linting/Formatting**: Use Ruff (`pyproject.toml` configured).
    ```bash
    uv run ruff check .
    uv run ruff format .
    ```
*   **Testing**: Use Pytest. *(Tests are not yet implemented)*.
    ```bash
    # Placeholder command, add tests to tests/ directory
    # uv run pytest
    ```
    *   Tests should be added under a `tests/` directory, mirroring the `sqlmcp` structure. Follow standard Pytest conventions.

## Contributing

This is primarily an example repository. Contributions improving the clarity, correctness, or demonstrating best practices for MCP server development are welcome via Pull Requests. Please ensure code is formatted and linted before submitting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details or visit [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

