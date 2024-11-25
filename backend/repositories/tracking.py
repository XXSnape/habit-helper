from datetime import date

from sqlalchemy import select

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from models import TrackingModel
from repositories.repository import ManagerRepository


class TrackingRepository(ManagerRepository):
    model = TrackingModel

    @classmethod
    async def get_end_date_habit(cls, session: AsyncSession, habit_id: int) -> date:
        query = select(func.max(cls.model.date)).filter_by(habit_id=habit_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
