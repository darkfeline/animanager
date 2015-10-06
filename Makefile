all:
	@echo "make publish - Publish to PyPi"

publish:
	rm dist/*
	python3 setup.py sdist
	python setup.py bdist_wheel
	python setup.py register
	twine upload dist/*

.PHONY: all publish
