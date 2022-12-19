SHELL := /bin/bash -O globstar


run_dev: check_env
	@ docker-compose up -d; \
	trap 'docker-compose down' INT; \
	ENV=development \
	   hypercorn --reload --config=hypercorn.toml '{{cookiecutter.project_slug}}.main:app'


test: check_env
	@ scripts/test_project.py


lint:
	@echo
	blue --check --diff --color .
	@echo
	ruff .
	@echo
	mypy .
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	blue .


build:
	docker build -t {{cookiecutter.project_slug}} .


smoke_test: build check_env
	@ scripts/smoke_test.py


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi
