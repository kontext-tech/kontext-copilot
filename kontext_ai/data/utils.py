from sqlalchemy import Engine, create_engine

from kontext_ai.utils import DB_URL

_engine: Engine = None


def get_engine() -> Engine:
    """Get the database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URL, echo=False)
    return _engine
