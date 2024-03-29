from typing import List
from pymongo.database import Database

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from .crud import VerificationConfigCRUD
from .models import (
    VerificationConfig,
    VerificationConfigPatch,
    VerificationConfigRead,
)
from ..core.auth import get_api_key
from ..core.models import GenericErrorMessage, StatusMessage
from ..db.session import get_db

router = APIRouter()


@router.post(
    "/",
    response_description="Add new verifier configuration",
    status_code=http_status.HTTP_201_CREATED,
    response_model=VerificationConfig,
    responses={http_status.HTTP_409_CONFLICT: {"model": GenericErrorMessage}},
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def create_ver_config(
    ver_config: VerificationConfig, db: Database = Depends(get_db)
):
    return await VerificationConfigCRUD(db).create(ver_config)


@router.get(
    "/",
    status_code=http_status.HTTP_200_OK,
    response_model=List[VerificationConfigRead],
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def get_all_ver_configs(db: Database = Depends(get_db)):
    return await VerificationConfigCRUD(db).get_all()


@router.get(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    responses={http_status.HTTP_404_NOT_FOUND: {"model": GenericErrorMessage}},
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def get_ver_conf(ver_config_id: str, db: Database = Depends(get_db)):
    return await VerificationConfigCRUD(db).get(ver_config_id)


@router.patch(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=VerificationConfigRead,
    responses={http_status.HTTP_404_NOT_FOUND: {"model": GenericErrorMessage}},
    response_model_exclude_unset=True,
    dependencies=[Depends(get_api_key)],
)
async def patch_ver_conf(
    ver_config_id: str,
    data: VerificationConfigPatch,
    db: Database = Depends(get_db),
):
    return await VerificationConfigCRUD(db).patch(
        ver_config_id=ver_config_id, data=data
    )


@router.delete(
    "/{ver_config_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=StatusMessage,
    responses={http_status.HTTP_404_NOT_FOUND: {"model": GenericErrorMessage}},
    dependencies=[Depends(get_api_key)],
)
async def delete_ver_conf_by_uuid(ver_config_id: str, db: Database = Depends(get_db)):
    status = await VerificationConfigCRUD(db).delete(ver_config_id)
    return StatusMessage(status=status, message="The verifier config was deleted")
