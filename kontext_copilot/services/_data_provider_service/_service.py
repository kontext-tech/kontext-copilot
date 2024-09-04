from kontext_copilot.data.models import DataSourceType
from kontext_copilot.data.schemas import DataSourceModel
from kontext_copilot.services._data_provider_service._provider import BaseProvider


class DataProviderService:
    """
    Data provider service class to perform operations on data sources:
    - Get data provider via data source id
    - Get data source schemas

    """

    @staticmethod
    def get_data_provider(source: DataSourceModel):
        """
        Get the data provider based on the data source type.
        """
        supported_types = [
            DataSourceType.SQLite,
            DataSourceType.DuckDB,
            DataSourceType.SQLServer,
        ]
        if source.type in supported_types:
            return BaseProvider(source)
        else:
            raise ValueError(f"Unsupported data source type: {source.type}")
