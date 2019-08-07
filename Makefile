cov:
	pytest --cov-report term-missing --cov-branch --cov=ambience tests/

lint:
	black -S -t py37 -l 79 chitanda tests
	isort -rc chitanda tests
	flake8 chitanda tests

tests:
	pytest tests/
	black -S -t py37 -l 79 --check chitanda tests
	isort -rc -c chitanda tests
	flake8 chitanda tests

.PHONY: cov lint tests
