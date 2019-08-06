cov:
	poetry run pytest --cov-report term-missing --cov-branch --cov=ambience tests/

lint:
	black -S -t py37 -l 79 chitanda
	poetry run isort -rc chitanda
	poetry run flake8 chitanda

test:
	poetry run pytest tests/
	black -S -t py37 -l 79 --check chitanda
	poetry run isort -rc -c .
	poetry run flake8

.PHONY: cov lint test
