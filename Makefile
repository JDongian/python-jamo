PROJECT=jamo
PYTHON := /usr/bin/env python
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print(sys.version_info[0])')
JAMO_VERSION=$(shell $(PYTHON) -c 'import jamo; print(jamo.__version__)')

default:
	@echo "install: install the package and scripts"
	@echo "clean: remove build/test artifacts"
	@echo "lint: check syntax"
	@echo "test: run unit tests"
	@echo "Python Version: $(PYTHON_VERSION)"
	@echo "  Jamo Version: $(JAMO_VERSION)"

install:
	python setup.py install

clean:
	find . -name \*.pyc -exec rm -f {} \;
	find . -depth -type d -name __pycache__ -exec rm -rf {} \;
	rm -rf build dist $(PROJECT).egg-info

lint:
	flake8 --ignore=E123,E501 $(PROJECT)

test:
	nosetests --with-coverage --cover-package=$(PROJECT)

dist/jamo-$(JAMO_VERSION).tar.gz:
	$(PYTHON) setup.py sdist
