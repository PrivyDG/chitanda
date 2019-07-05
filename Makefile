lint:
	poetry run isort -rc snowball
	poetry run flake8 snowball
build:
	poetry run poetry-setup .

.PHONY: lint build
