SHELL := /usr/bin/env bash

.PHONY: init lint test

help:
	@echo "init - Setup repo"
	@echo "lint - run linter and formatter checks"
	@echo "test - run unit tests"

init:
	pyenv virtualenv 3.10.5 h3xonize && pyenv local h3xonize

lint:
	poetry run pre-commit run --all-files

test:
	poetry run pytest -vv tests --cov=h3xonize --cov-report term-missing
