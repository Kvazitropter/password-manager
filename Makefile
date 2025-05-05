make setup:
	uv sync --no-dev
make setup-dev:
	uv sync
lint:
	uv run ruff check .
lint-fix:
	uv run ruff check . --fix
test:
	uv run pytest -s
test-coverage:
	uv run pytest --cov
run:
	uv run app.py