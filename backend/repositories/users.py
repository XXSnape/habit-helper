from typing import Tuple, Any, Sequence

from sqlalchemy import select, null, Row
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel, HabitModel
from repositories.repository import ManagerRepository


class UserRepository(ManagerRepository):
    """
    Запросы для работы с информацией о пользователях
    """

    model = UserModel

    @classmethod
    async def get_users_habits_by_hour(
        cls, session: AsyncSession, hour: int
    ) -> Sequence[Row[tuple[int, int, str]]]:
        """
        Получает данные о пользователях и их привычках,
        время напоминаний которых равно hour

        :param session: сессия для работы с базой
        :param hour: время напоминания о привычке
        :return: список из телеграм id, id привычки и названия привычки
        """
        query = (
            select(cls.model.telegram_id, HabitModel.id, HabitModel.name)
            .join(HabitModel)
            .filter(
                HabitModel.notification_hour == hour,
                cls.model.is_active == True,
                HabitModel.is_frozen == False,
                HabitModel.completed_at == null(),
            )
            .order_by(cls.model.telegram_id)
        )
        result = await session.execute(query)
        return result.all()

    @classmethod
    async def get_user_info(
        cls, session: AsyncSession, user_id: int
    ) -> Row[tuple[Any, Any, Any]] | None:
        """
        Получает информацию о пользователе
        :param session: сессия для работы с базой
        :param user_id: id пользователя
        :return: имя пользователя, статус активности, дату регистрации
        """
        query = select(
            cls.model.username, cls.model.is_active, cls.model.date_of_registration
        ).filter_by(id=user_id)
        result = await session.execute(query)
        return result.first()
