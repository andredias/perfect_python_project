SHELL := /bin/bash -O globstar


run:
	hypercorn --reload --config=hypercorn.toml '{{cookiecutter.project_slug}}.main:app'


test:
	pytest -x --cov-report term-missing --cov-report html --cov-branch \
	       --cov {{cookiecutter.project_slug}}/


lint:
	@echo
	isort --diff -c .
	@echo
	blue --check --diff --color .
	@echo
	flake8 .
	@echo
	mypy .
	@echo
	bandit -qr {{cookiecutter.project_slug}}/
	@echo
	pip-audit


format:
	isort .
	blue .
	pyupgrade --py{{cookiecutter.python_version.replace('.', '')}}-plus **/*.py


build:
	docker build -t {{cookiecutter.project_slug}} .


smoke_test: build
	docker run --rm -d -p 5000:5000 --name {{cookiecutter.project_slug}} {{cookiecutter.project_slug}}
	sleep 2; curl http://localhost:5000/hello
	docker stop {{cookiecutter.project_slug}}


install_hooks:
	@ scripts/install_hooks.sh
