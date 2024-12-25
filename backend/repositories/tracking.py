from datetime import date

from models import TrackingModel
from repositories.repository import ManagerRepository
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


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
