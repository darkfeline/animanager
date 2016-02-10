all:
	@echo "make publish - Publish to PyPi"

publish:
	rm dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	python3 setup.py register
	twine upload dist/*

.PHONY: all publish
