SHELL := /usr/bin/env bash -O globstar

run: check_env
	docker compose up --build


run_dev: check_env
	@ ENV=development docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build; \
	trap 'docker compose down' INT; \
	ENV=development poetry run ./entrypoint.sh


test: check_env
	docker compose up -d;
	pytest -x \
		--cov-report=term-missing --cov-report=html --cov-branch \
		--cov={{cookiecutter.project_slug}}


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


smoke_test: check_env
	@ scripts/smoke_test.py


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi
