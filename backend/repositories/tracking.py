from datetime import date

from sqlalchemy import select

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from models import TrackingModel
from repositories.repository import ManagerRepository


class TrackingRepository(ManagerRepository):
    """
    Запросы для работы с информацией о выполнении привычек
    """

    model = TrackingModel

    @classmethod
    async def get_end_date_habit(cls, session: AsyncSession, habit_id: int) -> date:
        """
        Получает максимальную дату, когда пользователь отмечал привычку
        :param session: сессия для работы с базой
        :param habit_id: id привычки
        :return: максимальная дата
        """
        query = select(func.max(cls.model.date)).filter_by(habit_id=habit_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
