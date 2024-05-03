.DEFAULT_GOAL := help
AUSTRAL_DATA_DIR = ./austral-data-sample
PROJECT = austral-lui
VENV_DIR = ${PROJECT}-env
PYTHON := python3
VENV_BIN = $(VENV_DIR)/bin/
VENV_PYTHON = $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest -vv
TESTDIR := tests

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
	@echo "make pytest: run the tests"
	@echo "make clean: remove the temporary files"
	@echo "make clean-packages: remove the installed packages"
	@echo "make clean-venv|cleanvenv: remove the virtual environment"
	@echo "make cleanall|clean-all: remove the virtual environment and the temporary files"

# .PHONY: install
# install: venv install-pypr2 install-asl install-austral-data-sample

.PHONY: install-pypr2
install-pypr2:
	@echo "Installing pypr2 in the virtual environment ..."
	@git clone git@gitlab-ssh.univ-lille.fr:loa/photons/pypr2.git
	@. $(VENV_DIR)/bin/activate && cd pypr2 && make && make install
	@echo "pypr2 successfully installed"

.PHONY: install-asl install-austral-sci-layer install-austral-scientific-layer install-lilas-web-processing
install-asl install-austral-sci-layer install-austral-scientific-layer install-lilas-web-processing:
	@echo "Installing austral-scientific-layer in the virtual environment ..."
	@git clone git@gitlab-ssh.univ-lille.fr:loa/agora/lilas-web-processing.git austral-scientific-layer
	@. $(VENV_DIR)/bin/activate && cd austral-scientific-layer && make && make install
	@echo "austral-scientific-layer successfully installed"

.PHONY: install-austral-data-sample install-ads
install-austral-data-sample install-ads:
	@echo "Installing austral-data-sample"
	@git clone git@gitlab-ssh.univ-lille.fr:loa/agora/austral-data-sample.git $(AUSTRAL_DATA_DIR)

.PHONY: venv austral-ui-env
venv austral-ui-env:
	@echo "Creating the virtual environment $(VENV_DIR) ..."
	@$(PYTHON) -m venv $(VENV_DIR) && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: venv install-pypr2 install-asl install-ads

.PHONY: pytest
pytest:
	$(PYTEST) $(TESTDIR)

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
