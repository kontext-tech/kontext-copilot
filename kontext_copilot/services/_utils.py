from sqlalchemy import Engine, create_engine

from kontext_copilot.utils import DB_URL, IS_DEV


class DatabaseEngine:
    _instance = None
    _engine: Engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            echo = True if IS_DEV else False
            self._engine = create_engine(
                DB_URL, echo=echo, pool_size=10, max_overflow=0
            )

    def _get_engine(self) -> Engine:
        return self._engine


def get_engine() -> Engine:
    """Get the database engine."""
    db_engine = DatabaseEngine()
    return db_engine._get_engine()
