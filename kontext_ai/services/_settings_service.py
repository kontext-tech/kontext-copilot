from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from kontext_ai.data.models import Setting
from kontext_ai.data.schemas import Settings
from kontext_ai.services._db_service import get_db_engine


class SettingsService:
    """
    SettingsService provides an interface for managing application settings stored in a database.
    It uses SQLAlchemy for database operations.

    Attributes:
        engine: An SQLAlchemy engine instance used to connect to the database.
        session: A sessionmaker instance bound to the engine for creating new database sessions.

    Methods:
        get_settings(): Retrieves all settings as a dictionary.
        get_setting(key): Retrieves the value of a setting by its key.
        set_setting(key, value): Sets the value of a setting identified by its key. Creates a new setting if it does not exist.

    """

    def __init__(self, engine):
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)

    def get_settings(self):
        """
        Retrieves all settings as a dictionary.

        Returns:
            dict: A dictionary containing all settings where the key is the setting key and the value is the setting value.
        """
        session = self.session()
        try:
            settings = session.query(Setting).all()
            return {setting.key: setting.value for setting in settings}
        finally:
            session.close()

    def get_settings_obj(self) -> Settings:
        """
        Retrieves all settings as a Settings object.
        """
        settings = self.get_settings()

        # Convert dictionary to class object
        return Settings(**settings)

    def get_setting(self, key):
        """
        Retrieves the value of a setting by its key.

        Parameters:
            key (str): The key of the setting to retrieve.

        Returns:
            str: The value of the setting if found, None otherwise.
        """
        session = self.session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            return setting.value if setting else None
        finally:
            session.close()

    def set_setting(self, key, value):
        """
        Sets the value of a setting identified by its key. Creates a new setting if it does not exist.

        Parameters:
            key (str): The key of the setting to set or create.
            value (str): The value to assign to the setting.

        Returns:
            None
        """
        session = self.session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                new_setting = Setting(key=key, value=value)
                session.add(new_setting)
            session.commit()
        finally:
            session.close()

    def delete_setting(self, key):
        """
        Deletes a setting by its key.

        Parameters:
            key (str): The key of the setting to delete.

        Returns:
            None
        """
        session = self.session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                session.delete(setting)
                session.commit()
        finally:
            session.close()


def get_settings_service(engine: Engine = Depends(get_db_engine)) -> SettingsService:
    """
    Returns a SettingsService instance with the provided engine.

    Parameters:
        engine (Engine): An SQLAlchemy engine instance used to connect to the database.

    Returns:
        SettingsService: An instance of SettingsService.
    """
    return SettingsService(engine)
