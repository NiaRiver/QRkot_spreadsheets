from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import charity_projects_crud, dontions_crud
from app.models.user import User
from app.schemas.donations import (
    DonationCreate, DonationRepresintation, SUDonationRepresintation
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    "/my/",
    response_model=list[DonationRepresintation],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await dontions_crud.get_own_donations(
        user.id,
        session
    )
    return new_donation.all()


@router.get(
    "/",
    response_model=list[SUDonationRepresintation],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await dontions_crud.get_all(session)


@router.post(
    "/",
    response_model=DonationRepresintation,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation = await dontions_crud.create(
        donation, False, user, session=session
    )
    session.add_all(
        invest(
            donation,
            await charity_projects_crud.get_all_open(
                session
            )
        )
    )
    await session.commit()
    await session.refresh(donation)
    return donation