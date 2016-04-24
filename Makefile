.PHONY: all
all: install

INSTALL_FLAGS=

.PHONY: install
install:
	python3 setup.py install ${INSTALL_FLAGS}

.PHONY: develop
develop:
	python3 setup.py develop ${INSTALL_FLAGS}

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

# Dev setup.
.PHONY: addhooks
addhooks:
	ln -s ../../hooks/pre-commit .git/hooks

# Run all checks.
.PHONY: check
check: test isort pylint

.PHONY: test
test:
	py.test --doctest-modules animanager tests

.PHONY: isort
isort:
	isort -rc animanager tests

.PHONY: pylint
pylint:
	pylint --output-format=colorized animanager tests || true
