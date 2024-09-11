import re

import duckdb

from kontext_copilot.data.models import DataSourceType
from kontext_copilot.data.schemas import DataSourceModel
from kontext_copilot.services._data_provider_service._provider import BaseProvider
from kontext_copilot.utils import get_db_path


class FileSourceProvider(BaseProvider):
    """
    Data provider for file sources.
    """

    def __init__(self, source: DataSourceModel) -> None:

        file_path = source.conn_str
        self.db_path = get_db_path(f"{source.id}_{source.type.value}_data.duckdb")
        self.file_type = source.type
        table_name = self._create_table_name(source.name)

        data_conn_str = f"duckdb:///{self.db_path}"

        self._add_table(table_name, file_path)

        super().__init__(
            DataSourceModel(
                id=source.id,
                name=source.name,
                conn_str=data_conn_str,
                conn_str_encrypted=False,
                type=source.type,
            )
        )

    def _create_table_name(self, name: str) -> str:
        """
        Create a table name from the source name and remove all special characters.
        """
        return re.sub(r"\W+", "_", name)

    def _add_table(self, table_name: str, path: str) -> None:
        """
        Add a table to the database.
        """
        with duckdb.connect(self.db_path) as conn:
            sql = (
                f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM read_csv(?, normalize_names=true)'
                if self.file_type == DataSourceType.CSV
                else (
                    f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM read_parquet(?, normalize_names=true)'
                    if self.file_type == DataSourceType.Parquet
                    else None
                )
            )
            if sql is not None:
                conn.execute(
                    sql,
                    [path],
                )

    def supports_schema(self) -> bool:
        """
        Check if the provider supports schema operations.
        Returns True if supported, False otherwise.
        """
        return False
