.PHONY: sync smoke verify dump categorize test ruff fmt docker helm-lint

sync:
	uv sync

smoke:
	uv run python -c "import lunch_money_mcp.server as s; print('tools:', sorted(t.name for t in s.mcp._tool_manager.list_tools()))"

verify:
	uv run python scripts/verify.py

dump:
	uv run python scripts/dump.py

categorize:
	uv run python scripts/categorize.py

test:
	uv run pytest

ruff:
	uv run ruff check . && uv run ruff format --check .

fmt:
	uv run ruff check --fix . && uv run ruff format .

docker:
	docker build -t ghcr.io/coilysiren/lunch-money-k8s:dev .

helm-lint:
	helm lint chart
