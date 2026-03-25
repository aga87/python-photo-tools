lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

test:
	pytest

check: lint test