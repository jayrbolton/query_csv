.PHONY: test lint test-debug
pkg = query_csv

lint:
	poetry run flake8 && \
		poetry run bandit $(pkg) && \
		poetry run mypy $(pkg)

test: lint
	poetry run pytest --cov=./$(pkg) --cov-report=xml test && \
		poetry run coverage report

test-debug: lint
	# Run tests for debugging: more verbose, quit on first failure
	poetry run pytest --cov=./$(pkg) --cov-report=xml -vv -x test && \
		poetry run coverage report && \
		poetry run coverage html
