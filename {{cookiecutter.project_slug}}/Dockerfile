FROM python:{{cookiecutter.python_version}}-slim as builder
LABEL maintainer="{{cookiecutter.author}} <{{cookiecutter.email}}>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m venv /venv

ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate; \
    $POETRY_HOME/bin/poetry install --only main --no-interaction


FROM python:{{cookiecutter.python_version}}-slim as final

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody
COPY --chown=nobody:nogroup {{cookiecutter.project_slug}}/ ./{{cookiecutter.project_slug}}

CMD ["hypercorn", "--worker-class=uvloop", "--bind=0.0.0.0:5000", "--error-logfile=-", "{{cookiecutter.project_slug}}.main:app"]
