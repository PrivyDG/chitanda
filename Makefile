lint:
	poetry run isort -rc chitanda
	poetry run flake8 chitanda

build:
	poetry run poetry-setup .

.PHONY: lint build
