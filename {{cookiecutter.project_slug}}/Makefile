SHELL := /bin/bash -O globstar


run_dev: check_env
	@ docker compose up -d; \
	trap 'docker compose down' INT; \
	ENV=development python entrypoint.py


test: check_env
	docker compose up -d;
	pytest -x \
		--cov-report=term-missing --cov-report=html --cov-branch \
		--cov={{cookiecutter.project_slug}}


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


smoke_test: build check_env
	@ scripts/smoke_test.py


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi
