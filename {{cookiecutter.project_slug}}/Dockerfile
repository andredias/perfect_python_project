# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder
LABEL maintainer="André Felipe Dias <andref.dias@gmail.com>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ref: https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile

COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# ---------------------------------------------------------

FROM python:3.14-slim AS final

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder --chown=nobody:nogroup /app/.venv ./.venv
ENV PATH=/app/.venv/bin:${PATH}

COPY --chown=nobody:nogroup --exclude=pyproject.toml --exclude=uv.lock . ./

USER nobody

EXPOSE 5000

CMD ["./entrypoint.sh"]

# ---------------------------------------------------------

FROM python:{{cookiecutter.python_version}}-slim AS builder
LABEL maintainer="{{cookiecutter.author}} <{{cookiecutter.email}}>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# ---------------------------------------------------------

FROM python:{{cookiecutter.python_version}}-slim AS final

WORKDIR /app
COPY --from=builder --chown=nobody:nogroup /app/.venv ./.venv
ENV PATH=/app/.venv/bin:${PATH}

COPY --chown=nobody:nogroup --exclude=pyproject.toml --exclude=uv.lock . ./

USER nobody
EXPOSE 5000

CMD ["./entrypoint.sh"]
