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

lint:
	pylint animanager

.PHONY: all publish test lint
