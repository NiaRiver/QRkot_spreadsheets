from datetime import datetime as dt

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in, /,
        to_commit: bool = True,
        user: User = None,
        *,
        session: AsyncSession
    ):
        obj_in_data = obj_in.dict()
        obj_in_data["create_date"] = dt.now()
        obj_in_data["invested_amount"] = 0
        if user:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if to_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_all(
        self,
        session: AsyncSession
    ):
        db_objs = await session.scalars(
            select(self.model)
        )
        return db_objs.all()

    async def get_all_open(
        self,
        session: AsyncSession
    ):
        db_objs = await session.scalars(
            select(self.model)
        )
        return db_objs.all()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for key in obj_data:
            if key in update_data:
                setattr(db_obj, key, update_data[key])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
