from kontext_copilot.data.models import DataSourceType
from kontext_copilot.data.schemas import DataSourceModel
from kontext_copilot.services._data_provider_service._file_source_provider import (
    FileSourceProvider,
)
from kontext_copilot.services._data_provider_service._provider import BaseProvider


class DataProviderService:
    """
    Data provider service class to perform operations on data sources:
    - Get data provider via data source id
    - Get data source schemas

    """

    _instances = {}

    @staticmethod
    def get_data_provider(source: DataSourceModel):
        """
        Get the data provider based on the data source type.
        """
        base_provider_types = [
            DataSourceType.SQLite,
            DataSourceType.DuckDB,
            DataSourceType.SQLServer,
            DataSourceType.PostgreSQL,
            DataSourceType.Oracle,
        ]
        file_provider_types = [DataSourceType.CSV, DataSourceType.Parquet]

        if source.id in DataProviderService._instances:
            return DataProviderService._instances[source.id]

        if source.type in base_provider_types:
            provider = BaseProvider(source)
        elif source.type in file_provider_types:
            provider = FileSourceProvider(source)
        else:
            raise ValueError(f"Unsupported data source type: {source.type}")

        DataProviderService._instances[source.id] = provider
        return provider
