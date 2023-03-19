import asyncio
from pathlib import Path
from subprocess import run

from {{cookiecutter.project_slug}} import config
from {{cookiecutter.project_slug}}.resources import connect_database, Database

parent_path = Path(__file__).parent


async def migrate() -> None:
    """
    Wait for the database to be ready.
    """
    db = Database(config.DATABASE_URL)
    await connect_database(db)
    await db.disconnect()
    run('alembic upgrade head'.split(), cwd=parent_path)
    return


if __name__ == '__main__':
    asyncio.run(migrate())
