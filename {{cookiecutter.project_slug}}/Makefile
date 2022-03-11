test:
	pytest --cov-report term-missing --cov-report html --cov-branch \
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


define git_pre_commit
#!/bin/bash
cd $$(git rev-parse --show-toplevel)
poetry run make lint
endef
export git_pre_commit

define git_pre_push
#!/bin/bash
cd $$(git rev-parse --show-toplevel)
poetry run make test
endef
export git_pre_push

define hg_hooks
[hooks]
precommit.lint = (cd `hg root`; poetry run make lint)
pre-push.test = (cd `hg root`; poetry run make test)
endef
export hg_hooks

install_hooks:
	@ if [ -d '.git' ]; then \
		echo "$$git_pre_commit" > .git/hooks/pre-commit; \
		echo "$$git_pre_push" > .git/hooks/pre-push; \
		chmod +x .git/hooks/pre-*; \
	elif ! grep -s -q 'precommit.lint' '.hg/hgrc'; then \
		echo "$$hg_hooks" >> .hg/hgrc; \
	fi
