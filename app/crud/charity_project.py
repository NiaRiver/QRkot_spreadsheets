
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ):
        return await session.scalars(
            select(self.model).where(
                self.model.name == project_name
            )
        )

    async def get_projects_by_completion_rate(
        self,
        limit: int = 10,
        offset: int = 0, *
        session: AsyncSession
    ) -> list[CharityProject]:
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.description,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label("open_duration")
            ).where(CharityProject.fully_invested).order_by("open_duration")
            .limit(limit)
            .offset(offset)
        )
        return projects.fetchall()


charity_projects_crud = CRUDCharityProject(CharityProject)
