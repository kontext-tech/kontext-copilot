import os
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from kontext_copilot.data.models import DataSource, DataSourceType
from kontext_copilot.data.schemas import (
    DataSourceCreateModel,
    DataSourceModel,
    DataSourceUpdateModel,
)
from kontext_copilot.services._utils import get_engine
from kontext_copilot.utils import get_logger

logger = get_logger()


class DataSourceService:
    """
    Provides services for creating and retrieving DataSource entities.
    This service utilizes SQLAlchemy for ORM operations.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the DataSourceService with a given database engine.

        :param engine: The SQLAlchemy engine to be used for database operations.
        """
        self.engine = engine
        self.session_maker = sessionmaker(bind=self.engine)

    def create_data_source(
        self, data_source_create: DataSourceCreateModel
    ) -> DataSourceModel:
        """
        Creates a new DataSource entity from a DataSourceCreateModel.

        :param data_source_create: The DataSourceCreateModel instance containing the data for the new DataSource.
        :return: The created DataSourceModel instance.
        """
        with self.session_maker() as session:
            # Convert DataSourceCreateModel to DataSource, assuming model_dump() correctly prepares data for creation
            new_data_source = DataSource(**data_source_create.model_dump())
            # Add the new DataSource to the session and commit changes
            session.add(new_data_source)
            session.commit()
            # Refresh the instance from the database to ensure it's up-to-date
            session.refresh(new_data_source)
            return new_data_source

    def get_data_source(self, data_source_id: int) -> Optional[DataSourceModel]:
        """
        Retrieves a DataSource entity by its ID.

        :param data_source_id: The ID of the DataSource to retrieve.
        :return: The DataSourceModel instance if found, otherwise None.
        """
        with self.session_maker() as session:
            # Query the DataSource by ID and return the result
            db_model = (
                session.query(DataSource)
                .filter(DataSource.id == data_source_id)
                .first()
            )
            if db_model:
                # Convert database model to Pydantic model
                return DataSourceModel.from_db_model(db_model)
            return None

    def get_all_data_sources(self) -> List[DataSourceModel]:
        with self.session_maker() as session:
            return [
                DataSourceModel.from_db_model(db_model)
                for db_model in session.query(DataSource).all()
            ]

    def update_data_source(
        self, data_source_id: int, data_source_update: DataSourceUpdateModel
    ) -> Optional[DataSourceModel]:
        """
        Updates an existing DataSource entity with new data.

        :param data_source_id: The ID of the DataSource to update.
        :param data_source_update: The DataSourceUpdateModel instance containing the updated data.
        :return: The updated DataSourceModel instance if the DataSource exists, otherwise None.
        """
        with self.session_maker() as session:
            data_source = (
                session.query(DataSource)
                .filter(DataSource.id == data_source_id)
                .first()
            )
            if data_source:
                update_data = data_source_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(data_source, key, value)
                session.commit()
                session.refresh(data_source)
                return DataSourceModel.from_db_model(data_source)
            return None

    def delete_data_source(self, data_source_id: int) -> Optional[DataSourceModel]:
        """
        Deletes a DataSource entity by its ID.

        :param data_source_id: The ID of the DataSource to delete.
        :return: The DataSourceModel instance that was deleted if found, otherwise None.
        """
        with self.session_maker() as session:
            data_source = (
                session.query(DataSource)
                .filter(DataSource.id == data_source_id)
                .first()
            )
            if data_source:
                session.delete(data_source)
                session.commit()
                return DataSourceModel.from_db_model(data_source)
            return None

    def ensure_sample_db(self):
        """
        Ensures that the database contains sample data.
        """
        chinook_name = "Chinook"
        with self.session_maker() as session:
            # Check if there is a SQLite database named Chinbook
            chinook = (
                session.query(DataSource)
                .filter(
                    DataSource.type == DataSourceType.SQLite,
                    DataSource.name == chinook_name,
                )
                .first()
            )

            # Get the abs path of the Chinook SQLite database in ../data/Chinook_Sqlite.db
            chinook_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../data/Chinook_Sqlite.db")
            )

            if chinook is None:
                logger.info(
                    "Adding sample data source: Chinook; path = %s", chinook_path
                )
                sample_data = [
                    DataSource(
                        name=chinook_name,
                        description="This is a sample data source.",
                        type=DataSourceType.SQLite,
                        conn_str="sqlite:///{}".format(chinook_path),
                        conn_str_encrypted=False,
                    ),
                ]
                session.add_all(sample_data)
                session.commit()


def get_data_sources_service(
    engine: Engine = Depends(get_engine),
) -> DataSourceService:
    """
    Returns a DataSourceService instance with the provided engine.
    """
    return DataSourceService(engine)
