from abc import ABC
from typing import List, Optional
from sqlalchemy import Engine, Inspector, MetaData, Table, create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.schema import CreateTable
from kontext_ai.data.models import DataSourceType
from kontext_ai.data.schemas import DataSourceModel


class BaseProvider(ABC):
    """
    Base class for data source providers.
    """

    def __init__(self, source: DataSourceModel) -> None:
        self.source = source
        # Create engine
        self.engine = __class__.__create_engine(source.conn_str)
        self.inspector = Inspector.from_engine(self.engine)
        self.inspector.get_schema_names

    @classmethod
    def __create_engine(conn_str: str) -> Engine:
        return create_engine(conn_str)

    def get_engine(self) -> Engine:
        """
        Get the engine object.
        """
        return self.engine

    def get_source_type(self) -> DataSourceType:
        """
        Get the data source type.
        """
        return self.source.type

    def supports_schema(self) -> bool:
        """
        Check if the provider supports schema operations.
        Returns True if supported, False otherwise.
        """
        return self.get_source_type() not in [
            DataSourceType.SQLite,
        ]

    def get_schemas(self) -> Optional[List[str]]:
        """
        Get a list of schemas from the data source.
        """
        if not self.supports_schema():
            return self.inspector.get_schema_names()
        return None

    def get_schemas_tables(self) -> Optional[dict[str, List[str]]]:
        """
        Get a dictionary of schemas and their tables from the data source.
        """
        if not self.supports_schema():
            schemas = self.get_schemas()
            schema_tables = {}
            for schema in schemas:
                schema_tables[schema] = self.get_tables(schema)
            return schema_tables
        return None

    def get_tables(self, schema: str = None) -> List[str]:
        """
        Get a list of tables from the data source.
        """
        tables = self.inspector.get_table_names(schema=schema)
        return tables

    def get_table_info(self, table: str, schema: str = None) -> Table:
        """
        Get table information from the data source.
        """
        metadata = MetaData()
        return Table(table, metadata, autoload_with=self.engine, schema=schema)

    def get_columns_info(
        self, table: str, schema: str = None
    ) -> Optional[List[ReflectedColumn]]:
        """
        Get columns info from the data source.
        """
        metadata = MetaData()
        table = Table(table, metadata, autoload_with=self.engine, schema=schema)
        # Use inspector to get columns information
        return self.inspector.get_columns(table.name, schema=schema)

    def get_table_creation_sql(self, table: str, schema: str = None) -> str:
        """
        Get table creation SQL from the data source.
        """
        metadata = MetaData()
        table = Table(table, metadata, autoload_with=self.engine, schema=schema)
        create_table_sql = str(CreateTable(table).compile(self.engine))
        return create_table_sql

    def get_table_data(
        self, table: str, schema: str = None, record_count: Optional[int] = None
    ) -> list:
        """
        Get data from the data source.
        """
        sql = f"SELECT * FROM {table}"
        if schema is not None:
            sql = f"SELECT * FROM {schema}.{table}"
        return self.get_data(sql, record_count)

    def get_data(self, sql: str, record_count: Optional[int] = None) -> list:
        """
        Get data from the data source.
        """
        with self.engine.connect() as conn:
            result = conn.execute(sql)
            if record_count is None:
                return result.fetchall()
            else:
                return result.fetchmany(record_count)
