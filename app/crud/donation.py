from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    async def get_own_donations(
        self,
        user_id: int,
        session: AsyncSession,
    ):
        return await session.scalars(
            select(self.model).where(self.model.user_id == user_id)
        )


dontions_crud = CRUDDonation(Donation)
