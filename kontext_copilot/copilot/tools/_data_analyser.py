from enum import Enum

import duckdb
import duckdb.typing
import pyarrow as pa

from kontext_copilot.data.schemas import (
    ColumnStatsModel,
    QueryStatsModel,
    SessionMessageModel,
)
from kontext_copilot.utils import ANA_DB_PATH, ANA_DB_TABLE_PREFIX, ANA_DB_VIEW_PREFIX


class StatsColumns(str, Enum):
    COLUMN_NAME = "column_name"
    COLUMN_TYPE = "column_type"
    MIN = "min"
    MAX = "max"
    APPROX_UNIQUE = "approx_unique"
    AVG = "avg"
    STD = "std"
    Q25 = "q25"
    Q50 = "q50"
    Q75 = "q75"
    COUNT = "count"
    NULL_PERCENTAGE = "null_percentage"


class DataAnalyser:

    def __init__(
        self,
        message: SessionMessageModel,
        data: list[dict],
        max_unique_categorical: int = 256,
    ) -> None:
        self.view_name = f"{ANA_DB_VIEW_PREFIX}{message.session_id}_{message.id}"
        self.tabel_name = f"{ANA_DB_TABLE_PREFIX}{message.session_id}_{message.id}"
        self.data = pa.Table.from_pylist(data)
        self.max_unique_categorical = max_unique_categorical

    def analyse(self) -> QueryStatsModel:

        with duckdb.connect(database=ANA_DB_PATH) as conn:
            # register view
            conn.register(self.view_name, self.data)

            query_stats = QueryStatsModel(
                column_stats=[], cache_table_name=self.tabel_name
            )

            # get summarize of the view
            query_write = f"SUMMARIZE {self.view_name}"
            summary = conn.execute(query_write).fetch_arrow_table()

            # convert summary to list of ColumnStats
            for row in summary.to_pylist():
                query_stats.column_stats.append(
                    ColumnStatsModel(
                        column_name=row[StatsColumns.COLUMN_NAME],
                        column_type=row[StatsColumns.COLUMN_TYPE],
                        min_val=row[StatsColumns.MIN],
                        max_val=row[StatsColumns.MAX],
                        approx_unique=row[StatsColumns.APPROX_UNIQUE],
                        avg=row[StatsColumns.AVG],
                        std=row[StatsColumns.STD],
                        q25=row[StatsColumns.Q25],
                        q50=row[StatsColumns.Q50],
                        q75=row[StatsColumns.Q75],
                        count=row[StatsColumns.COUNT],
                        null_percentage=row[StatsColumns.NULL_PERCENTAGE],
                    )
                )

            # find categorical columns where unique values are less than max_unique_categorical and type is string
            query_stats.categorical_columns = [
                c.column_name
                for c in query_stats.column_stats
                if c.approx_unique <= self.max_unique_categorical
                and c.column_type == duckdb.typing.VARCHAR
            ]

            # find boolean columns
            query_stats.boolean_columns = [
                c.column_name
                for c in query_stats.column_stats
                if c.column_type == duckdb.typing.BOOLEAN
            ]

            # find date and timestamp columns
            query_stats.datetime_columns = [
                c.column_name
                for c in query_stats.column_stats
                if c.column_type in [duckdb.typing.DATE, duckdb.typing.TIMESTAMP]
            ]

            # find numerical columns
            # TODO: enhance this to include more types and also use std and other metrics to recommend
            query_stats.numerical_columns = [
                c.column_name
                for c in query_stats.column_stats
                if c.column_type
                in [
                    duckdb.typing.INTEGER,
                    duckdb.typing.BIGINT,
                    duckdb.typing.SMALLINT,
                    duckdb.typing.TINYINT,
                    duckdb.typing.FLOAT,
                    duckdb.typing.DOUBLE,
                    duckdb.typing.HUGEINT,
                ]
            ]

            # write view to disk
            query_write = (
                f"CREATE TABLE {self.tabel_name} AS SELECT * FROM {self.view_name}"
            )
            conn.execute(query_write)
            query_stats.cached = True

            # Drop view
            conn.execute(f"DROP VIEW {self.view_name}")

            return query_stats
