SHELL := /usr/bin/env bash -O globstar


run: check_env
	docker compose up --build


run_dev: check_env
	ENV=development docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build


test:
	pytest -x --cov-report term-missing --cov-report html --cov-branch \
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


smoke_test: check_env
	trap 'docker compose down' EXIT; \
	docker compose up --build -d; \
	sleep 4; \
	httpx https://localhost/hello --http2 --no-verify -v; \
	[ $$? -eq 0 ] || exit 1; \
	echo 'Smoke test passed!'; exit 0


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then \
		cp sample.env .env; \
		echo '.env created from sample.env'; \
	fi
