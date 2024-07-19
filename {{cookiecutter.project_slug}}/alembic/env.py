import asyncio
from logging.config import fileConfig

from databases import Database, DatabaseURL
from loguru import logger
from sqlalchemy import engine_from_config, pool

from alembic import context
from {{ cookiecutter.project_slug }} import config as app_config
from {{ cookiecutter.project_slug }}.models import *  # noqa: F403
from {{ cookiecutter.project_slug }}.models import metadata
from {{ cookiecutter.project_slug }}.resources import connect_database

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', app_config.DATABASE_URL)

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

    with context.begin_transaction():
        context.run_migrations()


async def create_database_if_inexistent() -> None:
    url = DatabaseURL(app_config.DATABASE_URL).replace(database='postgres')
    db_root = Database(url)
    await connect_database(db_root)
    try:
        stmt = 'select 1 from pg_database where datname = :name'
        values = {'name': app_config.DB_NAME}
        db_exists = await db_root.execute(stmt, values)
        if not db_exists:
            stmt = f'create database {app_config.DB_NAME}'
            logger.warning(stmt)
            await db_root.execute(stmt)
    finally:
        await db_root.disconnect()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    asyncio.run(create_database_if_inexistent())
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
