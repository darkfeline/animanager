all:
	@echo "make publish - Publish to PyPi"
	@echo "make test - Run tests"
	@echo "make lint - Lint code"

publish:
	rm dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	python3 setup.py register
	twine upload dist/*

test:
	python3 -m unittest discover

check:
	isort -rc animanager tests
	pylint animanager tests || true
	MYPYPATH=stubs mypy animanager tests || true

.PHONY: all publish test lint
