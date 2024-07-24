from kontext_ai.data.models import DataSourceType
from kontext_ai.data.providers._provider import BaseProvider
from kontext_ai.data.schemas import DataSourceModel


def get_data_provider(source: DataSourceModel):
    """
    Get the data provider based on the data source type.
    """
    if source.type == DataSourceType.SQLite:
        return BaseProvider(source)
    else:
        raise ValueError(f"Unsupported data source type: {source.type}")
