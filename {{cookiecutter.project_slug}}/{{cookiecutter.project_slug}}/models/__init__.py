from pathlib import Path
from typing import Any

from pydantic import BaseModel
from sqlalchemy import MetaData

metadata = MetaData()

# metadata.tables is only populated after all models are imported.
# see alembic/env.py for an example.
modules = Path(__file__).parent.glob('*.py')
__all__ = [p.stem for p in modules if p.is_file() and p.stem != '__init__']


def diff_models(from_: BaseModel, to_: BaseModel) -> dict[str, Any]:
    """
    Return a dict with differences of the second in relation to the first model.
    Useful for getting only the fields that have changed before an update,
    for example.
    """
    from_dict = from_.dict()
    to_dict = to_.dict(exclude_unset=True)
    return {k: v for k, v in to_dict.items() if from_dict.get(k) != v}
