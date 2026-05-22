FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY lunch_money_mcp ./lunch_money_mcp
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV LUNCH_MONEY_MCP_TRANSPORT=http
ENV LUNCH_MONEY_MCP_HOST=0.0.0.0
ENV LUNCH_MONEY_MCP_PORT=8080
EXPOSE 8080

# Run the installed console script directly. No `uv run` at runtime: as a
# non-root pod user uv cannot write its cache, and the venv is already built.
CMD ["/app/.venv/bin/lunch-money-mcp"]
