SHELL := /usr/bin/env bash -O globstar

test:
	pytest --cov-report term-missing --cov-report html --cov-branch \
	       --cov {{cookiecutter.project_slug}}/

lint:
	ruff check --diff .
	@echo
	ruff format --diff .
	@echo
	mypy .


format:
	ruff check --silent --exit-zero --fix .
	@echo
	ruff format .


audit:
	pip-audit


install_hooks:
	@ scripts/install_hooks.sh
