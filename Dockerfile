FROM python:3.12-slim

# Build argument for the port the server listens on
ARG PORT=8051
# Environment variable for the application to read the port
ENV MCP_PORT=${PORT}

WORKDIR /app

# Install base system dependencies (needed for psycopg/asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Install uv, the dependency manager
RUN pip install uv

# Create a virtual environment within the container
RUN python -m venv .venv
# Add venv bin to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy only dependency definition files first to leverage Docker cache
COPY pyproject.toml uv.lock* /app/

# Install dependencies using uv into the virtual environment
RUN uv pip install --no-cache -e .

# Copy the rest of the application code
# Changes below this line will not invalidate the dependency cache
COPY sqlmcp /app/sqlmcp

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the MCP server using uv within the venv
CMD ["uv", "run", "python", "sqlmcp/server.py"] 