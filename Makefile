PYTHON_INTERPRETER=python3
VENV_PATH=.venv

SANDBOX_DIR=sandbox
STATICFILES_DIR=$(SANDBOX_DIR)/static-sources

DJANGO_MANAGE_PATH=$(SANDBOX_DIR)/manage.py

PYTHON_BIN=$(VENV_PATH)/bin/python
PIP_BIN=$(VENV_PATH)/bin/pip
TOX_BIN=$(VENV_PATH)/bin/tox
TWINE_BIN=$(VENV_PATH)/bin/twine
DJANGO_MANAGE_BIN=$(PYTHON_BIN) $(DJANGO_MANAGE_PATH)
FLAKE_BIN=$(VENV_PATH)/bin/flake8
PYTEST_BIN=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD_BIN=$(PYTHON_BIN) sphinx_reload.py

DEMO_DJANGO_SECRET_KEY=samplesecretfordev
PACKAGE_NAME=django-firm-info
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=firm_info

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  clean                         -- to clean EVERYTHING (Warning)"
	@echo "  clean-var                     -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-doc                     -- to remove documentation builds"
	@echo "  clean-install                 -- to clean app installation"
	@echo "  clean-pycache                 -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  install                       -- to install app requirements with Virtualenv and Pip"
	@echo
	@echo "  run                           -- to run Django development server"
	@echo "  migrate                       -- to apply demo database migrations"
	@echo "  migrations                    -- to create new migrations for application after changes"
	@echo "  check-migrations              -- to check for pending migrations (do not write anything)"
	@echo "  check-django                  -- to run Django System check framework"
	@echo "  superuser                     -- to create a superuser for Django admin"
	@echo
	@echo "  po                            -- to update every PO files from app and sandbox sources for enabled languages"
	@echo "  mo                            -- to build MO files from app and sandbox PO files"
	@echo
	@echo "  docs                          -- to build documentation"
	@echo "  livedocs                      -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  flake                         -- to launch Flake8 checking"
	@echo "  test                          -- to launch base test suite using Pytest"
	@echo "  test-initial                  -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  tox                           -- to launch tests for every Tox environments"
	@echo "  freeze-dependencies           -- to write a frozen.txt file with installed dependencies versions"
	@echo "  quality                       -- to launch Flake8 checking and every tests suites"
	@echo
	@echo "  check-release                 -- to check package release before uploading it to PyPi"
	@echo "  release                       -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .tox
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache


clean-var:
	@echo ""
	@echo "====Cleaning var/ directory ===="
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean-install:
	@echo ""
	@echo "==== Cleaning installation ===="
	@echo ""
	rm -Rf $(PACKAGE_SLUG).egg-info
	rm -Rf $(VENV_PATH)
.PHONY: clean-install


clean-doc:
	@echo ""
	@echo "==== Clear documentation ===="
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-var clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP_BIN) install --upgrade pip
	$(PIP_BIN) install --upgrade setuptools
.PHONY: venv

create-var-dirs:
	@mkdir -p var/db
	@mkdir -p var/static/css
	@mkdir -p var/media
	@mkdir -p $(SANDBOX_DIR)/media
	@mkdir -p $(STATICFILES_DIR)/css
.PHONY: create-var-dirs

install: venv create-var-dirs
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
	$(PIP_BIN) install -e .[dev,quality,doc,release]
	${MAKE} migrate
.PHONY: install

migrations:
	@echo ""
	@echo "==== Making application migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) makemigrations $(APPLICATION_NAME)
.PHONY: migrations

migrate:
	@echo ""
	@echo "==== Apply pending migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) migrate
.PHONY: migrate

superuser:
	@echo ""
	@echo "==== Create new superuser ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) createsuperuser
.PHONY: superuser

po:
	@echo ""
	@echo "==== Updating PO from application ===="
	@echo ""
	@cd $(APPLICATION_NAME); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) makemessages -a --keep-pot --no-obsolete
	@echo ""
	@echo "==== Updating PO from sandbox ===="
	@echo ""
	@cd $(SANDBOX_DIR); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) makemessages -a --keep-pot --no-obsolete
.PHONY: po

mo:
	@echo ""
	@echo "==== Building MO from application ===="
	@echo ""
	@cd $(APPLICATION_NAME); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) compilemessages --verbosity 3
	@echo ""
	@echo "==== Building MO from sandbox ===="
	@echo ""
	@cd $(SANDBOX_DIR); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) compilemessages --verbosity 3
.PHONY: mo

run:
	@echo ""
	@echo "==== Running development server ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) runserver 0.0.0.0:8001
.PHONY: run

docs:
	@echo ""
	@echo "==== Build documentation ===="
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@echo "==== Watching documentation sources ===="
	@echo ""
	$(SPHINX_RELOAD_BIN)
.PHONY: livedocs

check-django:
	@echo ""
	@echo "==== Running Django System check framework ===="
	@echo ""
	$(DJANGO_MANAGE_BIN) check
.PHONY: check-django

check-migrations:
	@echo ""
	@echo "==== Checking for pending project applications models migrations ===="
	@echo ""
	$(DJANGO_MANAGE_BIN) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

flake:
	@echo ""
	@echo "==== Running Flake check ===="
	@echo ""
	$(FLAKE_BIN) --statistics --show-source $(APPLICATION_NAME) sandbox tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Running Tests ===="
	@echo ""
	$(PYTEST_BIN) -vv --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@echo "==== Running Tests from zero ===="
	@echo ""
	$(PYTEST_BIN) -vv --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

freeze-dependencies:
	@echo ""
	@echo "==== Freezing backend dependencies versions ===="
	@echo ""
	$(PYTHON_BIN) freezer.py
.PHONY: freeze-dependencies

tox:
	@echo ""
	@echo "==== Launching tests with Tox environments ===="
	@echo ""
	$(TOX_BIN)
.PHONY: tox

build-package:
	@echo ""
	@echo "==== Building package ===="
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@echo "==== Releasing ===="
	@echo ""
	$(TWINE_BIN) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@echo "==== Checking package ===="
	@echo ""
	$(TWINE_BIN) check dist/*
.PHONY: check-release

quality: flake check-migrations test-initial docs check-release freeze-dependencies
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
