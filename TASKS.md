# SQL MCP Demo Server - Task List

## Initial Setup & Core Implementation

- [x] Write initial `PLANNING.md` outlining project scope
- [x] Set up project structure (`sqlmcp/`, `pyproject.toml`, `.env.example`)
- [x] Initialize `FastMCP` server in `sqlmcp/server.py`
- [x] Implement basic database connection logic in `sqlmcp/database_management.py` using `asyncpg`
- [x] Implement MCP server lifespan management for DB connections
- [x] Define `users` table schema (as documented)
- [x] Implement `add_user`, `get_all_users`,`find_user_by_email` and `delete_user_by_email` MCP tools
- [x] Create `Dockerfile` for containerization
- [x] Write initial `README.md` with setup and usage instructions


## Future Enhancements & Pending Tasks

- [ ] Implement comprehensive unit tests using `pytest` for:
    - [ ] `database_management.py` functions
    - [ ] Each MCP tool (`add_user`, `get_all_users`, etc.)
- [ ] Implement optional request signing using `MCP_SIGNING_KEY` environment variable
- [ ] Enhance error handling within MCP tools (more specific error messages)
- [ ] Add Pydantic models for input validation in MCP tools
- [ ] Improve inline code documentation and add docstrings where missing
- [ ] Investigate more robust database connection pooling options
- [ ] Consider adding tools for more complex queries (e.g., name filtering)

## Discovered During Work

*(Add any new tasks identified during development here)*