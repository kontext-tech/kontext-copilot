from abc import ABC
from typing import List, Optional

from sqlalchemy import Engine, Inspector, MetaData, Table, create_engine, text
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.schema import CreateTable

from kontext_copilot.data.models import DataSourceType
from kontext_copilot.data.schemas import (
    ColumnInfoModel,
    DataSourceModel,
    SchemaTablesModel,
)


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
            DataSourceType.DuckDB,
        ]

    def get_schemas(self) -> Optional[List[str]]:
        """
        Get a list of schemas from the data source.
        """
        if self.supports_schema():
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
                # Check if there is any table in the schema
                tables = self.get_tables(schema)
                if not tables or len(tables) == 0:
                    continue
                schema_tables.append(
                    SchemaTablesModel(schema_name=schema, tables=tables)
                )
            return schema_tables
        else:
            schema_tables.append(
                SchemaTablesModel(schema_name=None, tables=self.get_tables())
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

    def get_all_tables_info(self, schema: Optional[str] = None) -> List[Table]:
        """
        Get all tables information from the data source.
        """
        metadata = MetaData()
        tables = []
        if schema is None:
            schemas = self.get_schemas()
        else:
            schemas = [schema]
        if schemas is not None:
            for s in schemas:
                for table in self.get_tables(s):
                    tables.append(
                        Table(table, metadata, autoload_with=self.engine, schema=s)
                    )
        else:
            for table in self.get_tables(schema):
                tables.append(
                    Table(table, metadata, autoload_with=self.engine, schema=schema)
                )
        return tables

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
        table = Table(
            table,
            metadata,
            autoload_with=self.engine,
            schema=schema,
            quote=True,
            quote_schema=True,
        )
        create_table_sql = str(
            CreateTable(table, if_not_exists=True).compile(self.engine)
        )
        return create_table_sql

    def get_table_select_sql(
        self,
        table: str,
        schema: Optional[str] = None,
        record_count: Optional[int] = None,
    ) -> str:
        """
        Get table select SQL from the data source.
        """

        table_obj = Table(
            table,
            MetaData(),
            autoload_with=self.engine,
            schema=schema,
            quote=True,
            quote_schema=True,
        )
        statement = table_obj.select()
        if record_count is not None:
            statement = statement.limit(record_count)

        return str(
            statement.compile(self.engine, compile_kwargs={"literal_binds": True})
        )

    def get_table_data(
        self,
        table: str,
        schema: Optional[str] = None,
        record_count: Optional[int] = None,
    ) -> list[dict]:
        """
        Get data from the data source.
        """
        sql = f"SELECT * FROM {table}"
        if schema is not None:
            sql = f"SELECT * FROM {schema}.{table}"
        return self.run_sql(sql=sql, record_count=record_count)

    def run_sql(
        self, sql: str, schema: Optional[str] = None, record_count: Optional[int] = None
    ) -> list[dict]:
        """
        Get data from the data source.
        """
        with self.engine.connect() as conn:
            if schema is not None:
                conn.execute(f"USE {schema}")
            statement = text(sql)
            result = conn.execute(statement=statement)
            if result.returns_rows == False:
                # commit the transaction
                conn.commit()
                return [
                    {
                        "success": True,
                        "message": f"SQL statement executed successfully: {result.rowcount} rows affected",
                    }
                ]
            if record_count is None:
                rows = result.fetchall()
            else:
                rows = result.fetchmany(record_count)
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            conn.commit()
            return data
