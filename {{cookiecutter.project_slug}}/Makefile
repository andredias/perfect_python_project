SHELL := /usr/bin/env bash -O globstar


run:
	ENV=development hypercorn --reload --config=hypercorn.toml '{{cookiecutter.project_slug}}.main:app'


test:
	pytest -x --cov-report term-missing --cov-report html --cov-branch \
	       --cov {{cookiecutter.project_slug}}/


lint:
	@echo
	ruff .
	@echo
	blue --check --diff --color .
	@echo
	mypy .
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	blue .


build:
	docker build -t {{cookiecutter.project_slug}} .


smoke_test: build
	docker run --rm -d -p 5000:5000 --name {{cookiecutter.project_slug}} {{cookiecutter.project_slug}}
	sleep 4; curl http://localhost:5000/hello
	docker stop {{cookiecutter.project_slug}}


install_hooks:
	@ scripts/install_hooks.sh
