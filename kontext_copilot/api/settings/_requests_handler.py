from fastapi import APIRouter, Depends, HTTPException
from kontext_copilot.services import SettingsService, get_settings_service
from kontext_copilot.data.schemas import SettingsModel, SettingModel
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["settings"],
    prefix="/api/settings",
    responses={404: {"description": "Not found"}},
)


logger = get_logger()


@router.get("/", response_model=SettingsModel)
async def get_settings(
    settings_service: SettingsService = Depends(get_settings_service),
):
    """
    Endpoint to retrieve all settings.

    Returns:
        JSON response containing all settings.
    """
    logger.info("Getting all settings")
    settings = settings_service.get_settings_obj()
    return settings


@router.get("/{key}")
async def get_setting(
    key: str, settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Endpoint to retrieve the value of a setting by its key.

    Parameters:
        key (str): The key of the setting to retrieve.

    Returns:
        JSON response containing the value of the setting or a 404 error if not found.
    """
    value = settings_service.get_setting(key)
    logger.info("Getting setting %s", key)
    if value is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": key, "value": value}


@router.post("/")
async def set_setting(
    setting: SettingModel,
    settings_service: SettingsService = Depends(get_settings_service),
):
    """
    Endpoint to set the value of a setting. Creates a new setting if it does not exist.

    Parameters:
        setting (Setting): The setting to update or create.

    Returns:
        JSON response confirming the setting has been updated or created.
    """
    key = setting.key
    value = setting.value
    logger.info("Setting %s to %s", key, value)
    settings_service.set_setting(key, value)
    logger.info("Setting %s updated", key)
    return {"message": f"Setting {setting.key} updated successfully"}


@router.delete("/{key}")
async def delete_setting(
    key: str, settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Endpoint to delete a setting by its key.

    Parameters:
        key (str): The key of the setting to delete.

    Returns:
        JSON response confirming the setting has been deleted.
    """
    logger.info("Deleting setting %s", key)
    settings_service.delete_setting(key)
    logger.info("Setting %s deleted", key)
    return {"message": f"Setting {key} deleted successfully"}
