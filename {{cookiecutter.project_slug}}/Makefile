SHELL := /usr/bin/env bash -O globstar


run:
	docker compose up --build


run_dev:
	ENV=development docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build


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


smoke_test:
	trap 'docker compose down' EXIT; \
	docker compose up --build -d; \
	sleep 4; \
	httpx https://localhost/api/hello --http2 --no-verify -v; \
	[ $$? -eq 0 ] || exit 1; \
	echo 'Smoke test passed!'; exit 0


install_hooks:
	@ scripts/install_hooks.sh
