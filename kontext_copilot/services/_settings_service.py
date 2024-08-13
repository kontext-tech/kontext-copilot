from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from kontext_copilot.data.models import Setting
from kontext_copilot.data.schemas import SettingsModel
from kontext_copilot.services._utils import get_engine


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
        self.session_maker = sessionmaker(bind=self.engine)

    def get_settings(self):
        """
        Retrieves all settings as a dictionary.

        Returns:
            dict: A dictionary containing all settings where the key is the setting key and the value is the setting value.
        """
        with self.session_maker() as session:
            settings = session.query(Setting).all()
            return {setting.key: setting.value for setting in settings}

    def get_settings_obj(self) -> SettingsModel:
        """
        Retrieves all settings as a Settings object.
        """
        settings = self.get_settings()

        settingsModel = SettingsModel()

        # Convert dictionary to class object
        # Check data type in settingsModel and convert string to the correct type
        for key, value in settings.items():
            if hasattr(settingsModel, key):
                # get type of the attribute
                attr_type = type(getattr(settingsModel, key))
                # convert value to the correct type
                if attr_type == int:
                    value = int(value)
                elif attr_type == float:
                    value = float(value)
                setattr(settingsModel, key, value)

        return settingsModel

    def get_setting(self, key):
        """
        Retrieves the value of a setting by its key.

        Parameters:
            key (str): The key of the setting to retrieve.

        Returns:
            str: The value of the setting if found, None otherwise.
        """
        with self.session_maker() as session:
            setting = session.query(Setting).filter_by(key=key).first()
            return setting.value if setting else None

    def set_setting(self, key, value):
        """
        Sets the value of a setting identified by its key. Creates a new setting if it does not exist.

        Parameters:
            key (str): The key of the setting to set or create.
            value (str): The value to assign to the setting.

        Returns:
            None
        """
        with self.session_maker() as session:

            settings = self.get_settings_obj()
            typed_value = value
            # Check data type in settingsModel and convert string to the correct type
            if hasattr(settings, key):
                # get type of the attribute
                attr_type = type(getattr(settings, key))
                # convert value to the correct type
                if attr_type == int:
                    typed_value = int(value)
                elif attr_type == float:
                    typed_value = float(value)

            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                setting.value = typed_value
            else:
                new_setting = Setting(key=key, value=typed_value)
                session.add(new_setting)
            session.commit()

    def delete_setting(self, key):
        """
        Deletes a setting by its key.

        Parameters:
            key (str): The key of the setting to delete.

        Returns:
            None
        """
        with self.session_maker() as session:
            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                session.delete(setting)
                session.commit()


def get_settings_service(engine: Engine = Depends(get_engine)) -> SettingsService:
    """
    Returns a SettingsService instance with the provided engine.

    Parameters:
        engine (Engine): An SQLAlchemy engine instance used to connect to the database.

    Returns:
        SettingsService: An instance of SettingsService.
    """
    return SettingsService(engine)
