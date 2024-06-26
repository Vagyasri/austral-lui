.DEFAULT_GOAL := install
AUSTRAL_DATA_DIR = ./austral-data-sample
PROJECT = austral-lui
VENV_DIR = ${PROJECT}-env
PYTHON := python3
VENV_BIN = $(VENV_DIR)/bin
VENV_PYTHON = $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest -vv
TESTDIR := tests
PROJECT_ROOT := $(shell pwd)

.PHONY: help
help:
	@echo "make: show the default goal; for the time being, it is the help"
	@echo "make help: show this help"
	@echo "make install: install the project ${PROJECT}"
	@echo "make install-pypr2: install pypr2"
	@echo "make install-asl|install-austral-sci-layer|install-austral-scientific-layer|install-lilas-web-processing: install austral-scientific-layer"
	@echo "make install-austral-data-sample: install austral-data-sample"
	@echo "make venv|austral-ui-env: create a virtual environment and install the dependencies"
	@echo "make install-dev: install the development dependencies"
	@echo "make install-pkg: install the packages"
	@echo "make run: run the project"
	@echo "make pytest|test|tests: run the tests"
	@echo "make xtest: run an individual test | How to run it: eg: make xtest TEST=tests/test_licel_treatment.py"
	@echo "make clean: remove the temporary files"
	@echo "make clean-packages: remove the installed packages"
	@echo "make clean-venv|cleanvenv: remove the virtual environment"
	@echo "make cleanall|clean-all: remove the virtual environment and the temporary files"

.PHONY: install
install: venv install-pkg
	@echo "Do you want to install the austral-data-sample? [y/N]"
	@read -r answer; \
	if [ "$$answer" = "y" ]; then \
		make install-austral-data-sample; \
	fi

.PHONY: run
run:
	$(VENV_PYTHON) main.py

.PHONY: install-pypr2
install-pypr2:
	@echo "Installing pypr2 in the virtual environment $(VENV_DIR) ..."
	@git clone git@gitlab-ssh.univ-lille.fr:loa/photons/pypr2.git
	@cd pypr2 && make
	@$(PIP) install pypr2/dist/*.whl
	@echo "pypr2 successfully installed"

.PHONY: install-asl install-austral-sci-layer install-austral-scientific-layer install-lilas-web-processing
install-asl install-austral-sci-layer install-austral-scientific-layer install-lilas-web-processing:
	@echo "Installing austral-scientific-layer in the virtual environment $(VENV_DIR) ..."
	@git clone git@gitlab-ssh.univ-lille.fr:loa/agora/lilas-web-processing.git austral-scientific-layer
	@cd austral-scientific-layer && make
	@$(PIP) install austral-scientific-layer/dist/*.whl
	@echo "austral-scientific-layer successfully installed"

.PHONY: install-austral-data-sample install-ads install-samples
install-austral-data-sample install-ads install-samples:
	@echo "Installing austral-data-sample"
	@cd .. && git clone git@gitlab-ssh.univ-lille.fr:loa/agora/austral-data-sample.git $(AUSTRAL_DATA_DIR) && cd $(PROJECT)

.PHONY: venv austral-ui-env
venv austral-ui-env:
	@echo "Creating the virtual environment $(VENV_DIR) ..."
	@$(PYTHON) -m venv $(VENV_DIR) && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: venv install-pypr2 install-asl install-austral-data-sample

.PHONY: install-pkg
install-pkg: venv install-pypr2 install-asl

.PHONY: pytest test tests
pytest test tests:
	PYTHONPATH=$(PROJECT_ROOT) $(PYTEST) $(TESTDIR)

.PHONY: xtest
xtest:
	@PYTHONPATH=$(PROJECT_ROOT) $(PYTEST) $(TEST)

.PHONY: clean
clean:
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: clean-packages
clean-packages:
	@echo "Removing the installed packages ..."
	@rm -rf pypr2 austral-scientific-layer austral-data-sample

.PHONY: clean-venv cleanvenv
clean-venv cleanvenv:
	@echo "Removing the virtual environment $(VENV_DIR) ..."
	@rm -rf $(VENV_DIR)

.PHONY: cleanall clean-all
cleanall clean-all: clean cleanvenv clean-packages
