from sqlalchemy import create_engine
from kontext_copilot.services._singleton import SingletonMeta
from kontext_copilot.utils import DB_URL


class DbEngine(metaclass=SingletonMeta):

    def __init__(self):
        self.engine = create_engine(DB_URL)

    def get_engine(self):
        return self.engine


def get_db_engine():
    return DbEngine().get_engine()
