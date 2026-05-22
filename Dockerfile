FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY lunch_money_mcp ./lunch_money_mcp
RUN uv sync --frozen --no-dev

ENV LUNCH_MONEY_MCP_TRANSPORT=http
ENV LUNCH_MONEY_MCP_HOST=0.0.0.0
ENV LUNCH_MONEY_MCP_PORT=8080
EXPOSE 8080

CMD ["uv", "run", "--no-dev", "lunch-money-mcp"]
