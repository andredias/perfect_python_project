run:
	@ docker-compose up -d; \
	trap 'docker-compose down' INT; \
	hypercorn --reload --config=hypercorn.toml '{{cookiecutter.project_slug}}.main:app'


test:
	@ scripts/test_project.py


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
	docker-compose -f docker-compose.yml -f docker-compose.smoke_test.yml up -d
	sleep 2; curl http://localhost:5000/hello
	docker-compose -f docker-compose.yml -f docker-compose.smoke_test.yml down



install_hooks:
	@ scripts/install_hooks.sh
