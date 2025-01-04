from typing import Any

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_projects_crud
from app.services import google_api

router = APIRouter()


@router.post(
    "/",
    response_model=dict[str, Any],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    reservations = await charity_projects_crud.get_projects_by_completion_rate(
        limit, offset, session=session
    )
    spreadsheet_id, spreadsheet_url = await google_api.spreadsheets_create(
        wrapper_services
    )
    await google_api.set_user_permissions(spreadsheet_id, wrapper_services)
    updated_cells = await google_api.spreadsheets_update_value(
        spreadsheet_id,
        reservations,
        wrapper_services
    )
    response = dict(
        spreadsheet_id=spreadsheet_id,
        spreadsheet_url=spreadsheet_url,
        updates=updated_cells
    )
    return response
