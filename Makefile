.PHONY: all
all:
	@echo "make publish - Publish to PyPi"
	@echo "make test - Run tests"
	@echo "make lint - Lint code"

.PHONY: publish
publish:
	rm dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	python3 setup.py register
	twine upload dist/*

.PHONY: test
test:
	nosetests --with-doctest

.PHONY: check
check: isort pylint mypy

.PHONY: isort
isort:
	isort -rc animanager tests
	find stubs -name "*.pyi" -print0 | xargs -0 isort

.PHONY: pylint
pylint:
	pylint animanager tests || true

.PHONY: mypy
mypy:
	MYPYPATH=stubs mypy animanager || true
