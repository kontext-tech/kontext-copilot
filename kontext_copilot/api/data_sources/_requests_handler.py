from typing import List
from fastapi import APIRouter, Depends, HTTPException

from kontext_copilot.data.schemas import (
    DataSourceModel,
    DataSourceCreateModel,
    DataSourceUpdateModel,
)
from kontext_copilot.services import DataSourceService, get_data_sources_service
from kontext_copilot.utils import get_logger


router = APIRouter(
    tags=["data"],
    prefix="/api/data-sources",
    responses={
        404: {"description": "Not found"},
    },
)


logger = get_logger()


@router.post("/", response_model=DataSourceModel, status_code=201)
def create_data_source(
    data_source_create: DataSourceCreateModel,
    service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Create a new data source.
    """
    try:
        logger.info(f"Creating data source with details: {data_source_create}")
        return service.create_data_source(data_source_create)
    except Exception as e:
        logger.error(f"Error creating data source: {e}")
        raise HTTPException(status_code=500, detail="Error creating data source")


@router.get("/", response_model=List[DataSourceModel])
def get_all_data_sources(
    service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Retrieve all data sources.
    """
    try:
        logger.info("Retrieving all data sources")
        return service.get_all_data_sources()
    except Exception as e:
        logger.error(f"Error retrieving data sources: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data sources")


@router.get("/{data_source_id}", response_model=DataSourceModel)
def get_data_source(
    data_source_id: int,
    service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Retrieve a data source by its ID.
    """
    try:
        logger.info(f"Retrieving data source with ID: {data_source_id}")
        data_source = service.get_data_source(data_source_id)
        if data_source is None:
            raise HTTPException(status_code=404, detail="DataSource not found")
        return data_source
    except Exception as e:
        logger.error(f"Error retrieving data source with ID {data_source_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data source")


@router.put("/{data_source_id}", response_model=DataSourceModel)
def update_data_source(
    data_source_id: int,
    data_source_update: DataSourceUpdateModel,
    service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Update an existing data source.
    """
    try:
        logger.info(
            f"Updating data source with ID: {data_source_id} with details: {data_source_update}"
        )
        updated_data_source = service.update_data_source(
            data_source_id, data_source_update
        )
        if updated_data_source is None:
            raise HTTPException(status_code=404, detail="DataSource not found")
        return updated_data_source
    except Exception as e:
        logger.error(f"Error updating data source with ID {data_source_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating data source")


@router.delete("/{data_source_id}", response_model=DataSourceModel)
def delete_data_source(
    data_source_id: int,
    service: DataSourceService = Depends(get_data_sources_service),
):
    """
    Delete a data source by its ID.
    """
    try:
        logger.info(f"Deleting data source with ID: {data_source_id}")
        deleted_data_source = service.delete_data_source(data_source_id)
        if deleted_data_source is None:
            raise HTTPException(status_code=404, detail="DataSource not found")
        return deleted_data_source
    except Exception as e:
        logger.error(f"Error deleting data source with ID {data_source_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting data source")
