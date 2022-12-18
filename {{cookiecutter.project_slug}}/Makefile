SHELL := /bin/bash -O globstar

test:
	pytest --cov-report term-missing --cov-report html --cov-branch \
	       --cov {{cookiecutter.project_slug}}/

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


install_hooks:
	@ scripts/install_hooks.sh
