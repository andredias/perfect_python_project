SHELL := /bin/bash -O globstar

test:
	pytest --cov-report term-missing --cov-report html --cov-branch \
	       --cov {{cookiecutter.project_slug}}/

lint:
	@echo
	isort --diff -c .
	@echo
	blue --check --diff --color .
	@echo
	ruff .
	@echo
	mypy .
	@echo
	bandit -qr {{cookiecutter.project_slug}}/
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	isort .
	blue .
	pyupgrade --py{{cookiecutter.python_version.replace('.', '')}}-plus **/*.py


install_hooks:
	@ scripts/install_hooks.sh
