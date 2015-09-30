all:
	@echo "make build - Build distributions"
	@echo "make upload - Upload distributions to PyPi"
	@echo "make clean - Clean distributions"

build: sdist wheel

sdist:
	python3 setup.py sdist

wheel:
	python setup.py bdist_wheel

clean:
	rm dist/*

upload:
	twine upload dist/*

.PHONY: all build sdist wheel clean upload
