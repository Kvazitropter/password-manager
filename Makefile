setup:
	uv sync --no-dev
setup-dev:
	uv sync
lint:
	uv run ruff check .
lint-fix:
	uv run ruff check . --fix
test:
	uv run pytest -s -W ignore::DeprecationWarning
test-coverage:
	uv run pytest -W ignore::DeprecationWarning --cov=backend --cov=scripts --cov=frontend --cov-report=xml:coverage.xml
run:
	uv run app.py
build:
	pyinstaller password-manager.spec
run-linux:
	./dist/password-manager/password-manager
remove-linux:
	rm -rf build dist