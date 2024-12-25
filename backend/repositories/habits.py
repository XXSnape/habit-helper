from collections.abc import Sequence

from models import HabitModel, TrackingModel
from repositories.repository import ManagerRepository
from sqlalchemy import null, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class HabitRepository(ManagerRepository):
    """
    Запросы для работы с привычками
    """

    model = HabitModel

    @classmethod
    async def get_required_count(cls, session: AsyncSession, data: dict) -> int | None:
        """
        Запрашивает, сколько раз привычка должна выполняться
        :param session: сессия для работы с базой
        :param data: данные для фильтрации, которые должны однозначно идентифицировать 1 запись в базе
        :return: Количество, сколько раз привычка должна выполняться или None, если она не найдена
        """
        query = select(cls.model.count).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_habit_name(cls, session: AsyncSession, data: dict) -> str | None:
        """
        Возвращает название привычки
        :param session: сессия для работы с базой
        :param data: данные для фильтрации, которые должны однозначно идентифицировать 1 запись в базе
        :return: название привычки или None, если нет данных о привычке
        """
        query = select(cls.model.name).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_habits(
        cls,
        session: AsyncSession,
        user_id: int,
        is_complete_null: bool,
    ) -> Sequence[HabitModel]:
        """
        Возвращает информацию о привычках пользователя, как завершённых, так и действующих.
        Подгружает данные о дате выполнения, статусе (выполнена или нет), причину невыполнения
        :param session: сессия для работы с базой
        :param user_id: id пользователя
        :param is_complete_null: True, если нужны действующие привычки, иначе завершенные, False
        :return: данные о привычках пользователя
        """
        query = (
            select(cls.model)
            .options(
                selectinload(HabitModel.tracking).load_only(
                    TrackingModel.date, TrackingModel.is_done, TrackingModel.reason
                )
            )
            .filter_by(user_id=user_id)
            .order_by(cls.model.is_frozen.desc())
        )
        if is_complete_null:
            query = query.filter(cls.model.completed_at == null())
        else:
            query = query.filter(cls.model.completed_at != null())
        result = await session.execute(query)
        return result.scalars().all()
