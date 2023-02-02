FROM python:{{cookiecutter.python_version}}-slim as builder
LABEL maintainer="{{cookiecutter.author}} <{{cookiecutter.email}}>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://install.python-poetry.org | python -

RUN python -m venv /venv
ENV PATH=/venv/bin:/root/.local/bin:${PATH}

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate; \
    poetry install --no-dev

# ---------------------------------------------------------

FROM python:{{cookiecutter.python_version}}-slim as final


RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody
COPY --chown=nobody:nogroup entrypoint.py hypercorn.toml alembic.ini ./
COPY --chown=nobody:nogroup alembic/ ./alembic
COPY --chown=nobody:nogroup {{cookiecutter.project_slug}}/ ./{{cookiecutter.project_slug}}

EXPOSE 5000

CMD ["python", "entrypoint.py"]
