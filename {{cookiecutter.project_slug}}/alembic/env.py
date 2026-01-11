from logging.config import fileConfig
from urllib.parse import urlparse

from loguru import logger
from sqlalchemy import create_engine, engine_from_config, pool, text

from alembic import context
from {{ cookiecutter.project_slug }} import config as app_config
from {{ cookiecutter.project_slug }}.models import *  # noqa: F403
from {{ cookiecutter.project_slug }}.models import metadata
from {{ cookiecutter.project_slug }}.resources import init_database, test_database_connection, get_db



# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', app_config.DATABASE_URL.replace('+asyncpg', ''))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )


def create_database_if_inexistent() -> None:
    url = urlparse(app_config.DATABASE_URL)._replace(scheme='postgresql', path='postgres').geturl()
    engine = create_engine(url, echo=True)
    stmt = text('select 1 from pg_database where datname = :name')
    values = {'name': app_config.DB_NAME}
    conn = engine.connect()
    conn.execution_options(isolation_level="AUTOCOMMIT")
    try:
        db_exists = conn.execute(stmt, values).first() is not None
        if not db_exists:
            stmt = text(f'create database {app_config.DB_NAME}')
            logger.warning(stmt)
            conn.execute(stmt)
    finally:
        conn.close()
        engine.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    create_database_if_inexistent()
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
