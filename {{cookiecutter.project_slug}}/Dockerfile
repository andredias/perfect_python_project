FROM python:{{cookiecutter.python_version}}-slim as builder
LABEL maintainer="{{cookiecutter.author}} <{{cookiecutter.email}}>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m venv /venv

ENV POETRY_VERSION=1.4.1
ENV POETRY_HOME=/opt/poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV POETRY_VERSION=1.4.1
RUN curl https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate; \
    $POETRY_HOME/bin/poetry install --only main --no-interaction

# ---------------------------------------------------------

FROM python:{{cookiecutter.python_version}}-slim as final

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody
COPY --chown=nobody:nogroup entrypoint.sh migrate_database.py hypercorn.toml alembic.ini ./
COPY --chown=nobody:nogroup alembic/ ./alembic
COPY --chown=nobody:nogroup {{cookiecutter.project_slug}}/ ./{{cookiecutter.project_slug}}

EXPOSE 5000

CMD ["./entrypoint.sh"]
