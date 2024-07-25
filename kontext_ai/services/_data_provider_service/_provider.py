from abc import ABC
from typing import List, Optional
from sqlalchemy import Engine, Inspector, MetaData, Table, create_engine, text
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.schema import CreateTable
from kontext_ai.data.models import DataSourceType
from kontext_ai.data.schemas import DataSourceModel, SchemaTablesModel, ColumnInfoModel


class BaseProvider(ABC):
    """
    Base class for data source providers.
    """

    def __init__(self, source: DataSourceModel) -> None:
        self.source = source
        # Create engine
        self.engine = BaseProvider.__create_engine(source.conn_str)
        self.inspector = Inspector.from_engine(self.engine)
        self.inspector.get_schema_names

    @staticmethod
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

    def get_schemas_tables(self) -> List[SchemaTablesModel]:
        """
        Get a dictionary of schemas and their tables from the data source.
        """
        schema_tables = []
        if self.supports_schema():
            schemas = self.get_schemas()
            for schema in schemas:
                schema_tables.append(
                    SchemaTablesModel(schema=schema, tables=self.get_tables(schema))
                )
            return schema_tables
        else:
            schema_tables.append(
                SchemaTablesModel(schema=None, tables=self.get_tables())
            )
        return schema_tables

    def get_tables(self, schema: Optional[str] = None) -> List[str]:
        """
        Get a list of tables from the data source.
        """
        tables = self.inspector.get_table_names(schema=schema)
        return tables

    def get_table_info(self, table: str, schema: Optional[str] = None) -> Table:
        """
        Get table information from the data source.
        """
        metadata = MetaData()
        return Table(table, metadata, autoload_with=self.engine, schema=schema)

    def get_columns_info(
        self, table: str, schema: Optional[str] = None
    ) -> Optional[List[ColumnInfoModel]]:
        """
        Get columns info from the data source.
        """
        metadata = MetaData()
        tbl = Table(table, metadata, autoload_with=self.engine, schema=schema)

        # Use inspector to get columns information
        return [
            ColumnInfoModel(
                data_type=str(c.type),
                name=c.name,
                nullable=c.nullable,
                comment=c.comment,
                default=c.default,
                autoincrement=True if c.autoincrement == "auto" else False,
                primary_key=c.primary_key,
                index=c.index,
                unique=c.unique,
            )
            for c in tbl.columns
        ]

    def get_table_creation_sql(self, table: str, schema: Optional[str] = None) -> str:
        """
        Get table creation SQL from the data source.
        """
        metadata = MetaData()
        table = Table(table, metadata, autoload_with=self.engine, schema=schema)
        create_table_sql = str(CreateTable(table).compile(self.engine))
        return create_table_sql

    def get_table_data(
        self,
        table: str,
        schema: Optional[str] = None,
        record_count: Optional[int] = None,
    ) -> dict:
        """
        Get data from the data source.
        """
        sql = f"SELECT * FROM {table}"
        if schema is not None:
            sql = f"SELECT * FROM {schema}.{table}"
        return self.get_data(sql, record_count)

    def get_data(self, sql: str, record_count: Optional[int] = None) -> dict:
        """
        Get data from the data source.
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            if record_count is None:
                rows = result.fetchall()
            else:
                rows = result.fetchmany(record_count)
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            return data
