.PHONY: all
all: install

INSTALL_FLAGS=

.PHONY: install
install:
	python3 setup.py install ${INSTALL_FLAGS}

.PHONY: requirements
requirements:
	pip3 install ${INSTALL_FLAGS} -r requirements.txt

.PHONY: package
package:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

.PHONY: clean
clean:
	python3 setup.py clean --all
	rm -rf dist

# Publish to PyPi.
.PHONY: publish
publish: clean package
	python3 setup.py register
	twine upload dist/*

.PHONY: test
test:
	nosetests --with-doctest

# Run all checks.
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
