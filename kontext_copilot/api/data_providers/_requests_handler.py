import traceback
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException

from kontext_copilot.data.schemas import (
    DataProviderInfoModel,
    ColumnInfoModel,
    SqlStatementModel,
    RunSqlResultModel,
    RunSqlPostBodyModel,
)
from kontext_copilot.services import (
    DataProviderService,
    get_data_sources_service,
    DataSourceService,
)
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["data"],
    prefix="/api/data-providers",
    responses={
        404: {"description": "Not found"},
    },
)

logger = get_logger()


def get_data_provider(
    data_source_id: int,
    source_service: DataSourceService,
):
    """
    Get the data provider based on the data source id.
    """
    try:
        logger.info(f"Retrieving data provider for data source id: {data_source_id}")
        source = source_service.get_data_source(data_source_id)
        provider = DataProviderService.get_data_provider(source)
        return provider
    except Exception as e:
        logger.error(f"Error retrieving data provider (#{data_source_id}): {e}")
        raise e


@router.get("/{data_source_id}", response_model=DataProviderInfoModel)
def get_data_provider_info(
    data_source_id: int,
    source_service: DataSourceService = Depends(get_data_sources_service),
) -> DataProviderInfoModel:
    """
    Get the data provider based on the data source id.
    """
    try:
        source = source_service.get_data_source(data_source_id)
        provider = get_data_provider(data_source_id, source_service)
        return DataProviderInfoModel(
            **source.model_dump(),
            supports_schema=provider.supports_schema(),
            metadata=provider.get_schemas_tables(),
        )
    except Exception as e:
        logger.error(f"Error retrieving data provider (#{data_source_id}): {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data provider")


@router.get("/{data_source_id}/columns", response_model=List[ColumnInfoModel])
def get_columns(
    data_source_id: int,
    table: str,
    schema: Optional[str] = None,
    source_service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Get columns info from the data source.
    """
    try:
        logger.info(f"Retrieving columns info for table: {table}")
        provider = get_data_provider(data_source_id, source_service)
        return provider.get_columns_info(table, schema)
    except Exception as e:
        logger.error(f"Error retrieving columns info for table: {table}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving columns info")


@router.get("/{data_source_id}/table-creation-sql", response_model=SqlStatementModel)
def get_table_creation_sql(
    data_source_id: int,
    table: str,
    schema: Optional[str] = None,
    source_service: DataSourceService = Depends(get_data_sources_service),
) -> SqlStatementModel:
    """
    Get table creation SQL from the data source.
    """
    try:
        logger.info(f"Retrieving CREATE TABLE SQL for table: {table}")
        provider = get_data_provider(data_source_id, source_service)
        return SqlStatementModel(sql=provider.get_table_creation_sql(table, schema))
    except Exception as e:
        logger.error(f"Error retrieving CREATE TABLE SQL for table: {table}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving CREATE TABLE SQL")


@router.get("/{data_source_id}/table-select-sql", response_model=SqlStatementModel)
def get_table_creation_sql(
    data_source_id: int,
    table: str,
    schema: Optional[str] = None,
    record_count: Optional[int] = 10,
    source_service: DataSourceService = Depends(get_data_sources_service),
) -> SqlStatementModel:
    """
    Get table select SQL from the data source.
    """
    try:
        logger.info(f"Retrieving SELECT SQL for table: {table}")
        provider = get_data_provider(data_source_id, source_service)
        return SqlStatementModel(
            sql=provider.get_table_select_sql(table, schema, record_count)
        )
    except Exception as e:
        logger.error(f"Error retrieving SELECT SQL for table: {table}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving table SELECT SQL")


@router.get("/{data_source_id}/table-samples", response_model=List[dict])
def get_table_samples(
    data_source_id: int,
    table: str,
    schema: Optional[str] = None,
    record_count: Optional[int] = 10,
    source_service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Get table samples from the data source.
    """
    try:
        logger.info(f"Retrieving table samples for table: {table}")
        provider = get_data_provider(data_source_id, source_service)
        return provider.get_table_data(table, schema, record_count)
    except Exception as e:
        logger.error(f"Error retrieving table samples for table: {table}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving table samples")


@router.post("/{data_source_id}/run-sql", response_model=RunSqlResultModel)
def run_sql(
    data_source_id: int,
    payload: RunSqlPostBodyModel = Body(None),
    source_service: DataSourceService = Depends(get_data_sources_service),
) -> RunSqlResultModel:
    """
    Run SQL the data source.
    """
    try:
        sql = payload.sql
        schema = payload.schema_name
        record_count = payload.record_count
        logger.info(f"Run SQL: {sql}")
        provider = get_data_provider(data_source_id, source_service)
        data = provider.run_sql(sql=sql, record_count=record_count, schema=schema)
        return RunSqlResultModel(
            data=data, success=True, message="SQL executed successfully"
        )
    except Exception as e:
        logger.error(f"Error running SQL: {sql}; {e}")
        logger.error(traceback.format_exc())

        return RunSqlResultModel(
            data=[], success=False, message=f"Error running SQL: {sql}; {e}"
        )
