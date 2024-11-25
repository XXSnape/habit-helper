from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import HabitModel
from repositories.repository import ManagerRepository


class HabitRepository(ManagerRepository):
    model = HabitModel

    @classmethod
    async def get_required_count(cls, session: AsyncSession, data: dict) -> int | None:
        query = select(cls.model.count).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()
