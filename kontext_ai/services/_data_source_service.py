from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from kontext_ai.data.schemas import (
    DataSourceModel,
    DataSourceCreateModel,
    DataSourceUpdateModel,
)
from kontext_ai.data.models import DataSource


class DataSourceService:
    """
    Provides services for creating and retrieving DataSource entities.
    This service utilizes SQLAlchemy for ORM operations.
    """

    def __init__(self, engine):
        """
        Initializes the DataSourceService with a given database engine.

        :param engine: The SQLAlchemy engine to be used for database operations.
        """
        self.engine = engine
        self.db_session = sessionmaker(bind=self.engine)

    def create_data_source(
        self, data_source_create: DataSourceCreateModel
    ) -> DataSourceModel:
        """
        Creates a new DataSource entity from a DataSourceCreateModel.

        :param data_source_create: The DataSourceCreateModel instance containing the data for the new DataSource.
        :return: The created DataSourceModel instance.
        """
        # Convert DataSourceCreateModel to DataSource, assuming model_dump() correctly prepares data for creation
        new_data_source = DataSource(**data_source_create.model_dump())
        # Add the new DataSource to the session and commit changes
        self.db_session.add(new_data_source)
        self.db_session.commit()
        # Refresh the instance from the database to ensure it's up-to-date
        self.db_session.refresh(new_data_source)
        return new_data_source

    def get_data_source(self, data_source_id: int) -> Optional[DataSourceModel]:
        """
        Retrieves a DataSource entity by its ID.

        :param data_source_id: The ID of the DataSource to retrieve.
        :return: The DataSourceModel instance if found, otherwise None.
        """
        # Query the DataSource by ID and return the result
        db_model = (
            self.db_session.query(DataSource)
            .filter(DataSource.id == data_source_id)
            .first()
        )
        if db_model:
            # Convert database model to Pydantic model
            return DataSourceModel.from_db_model(db_model)
        return None

    def get_all_data_sources(self) -> List[DataSourceModel]:
        return [
            DataSourceModel.from_db_model(db_model)
            for db_model in self.db_session.query(DataSource).all()
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
        data_source = (
            self.db_session.query(DataSource)
            .filter(DataSource.id == data_source_id)
            .first()
        )
        if data_source:
            update_data = data_source_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(data_source, key, value)
            self.db_session.commit()
            self.db_session.refresh(data_source)
            return DataSourceModel.from_db_model(data_source)
        return None

    def delete_data_source(self, data_source_id: int) -> Optional[DataSourceModel]:
        """
        Deletes a DataSource entity by its ID.

        :param data_source_id: The ID of the DataSource to delete.
        :return: The DataSourceModel instance that was deleted if found, otherwise None.
        """
        data_source = (
            self.db_session.query(DataSource)
            .filter(DataSource.id == data_source_id)
            .first()
        )
        if data_source:
            self.db_session.delete(data_source)
            self.db_session.commit()
            return DataSourceModel.from_db_model(data_source)
        return None
