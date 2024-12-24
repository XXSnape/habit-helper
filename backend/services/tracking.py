from sqlalchemy.ext.asyncio import AsyncSession

from repositories.habits import HabitRepository
from repositories.tracking import TrackingRepository
from schemas.habits import MarkHabitSchema
from services.habits import end_habit, habit_not_exists
from utils.validations import check_date_format


async def mark_habit_by_id(
    session: AsyncSession, habit_id: int, mark: MarkHabitSchema
) -> bool:
    """
    Помечает ежедневное задание как выполненное или невыполненное.
    :param session: Сессия для работы с базой
    :param habit_id: id привычки в базе
    :param mark: MarkHabitSchema
    :return: результат операции
    """
    data = mark.model_dump(exclude_none=True)
    data["date"] = check_date_format(data["date"])
    data["habit_id"] = habit_id
    tracking_id = await TrackingRepository.create_object(session=session, data=data)
    return bool(tracking_id)


async def is_habit_complete(
    session: AsyncSession, habit_id: int, required_count: int
) -> bool:
    """
    Получает информацию о том, является ли привычка сформированной
    по количеству фактически выполненных заданий и тому, что указал пользователь
    :param session: сессия для работы с базой
    :param habit_id: id привычки в базе
    :param required_count: количество дней для формирования привычки
    :return: True, если привычка сформирована, иначе False
    """
    number_completed = await TrackingRepository.count_number_objects_by_params(
        session=session, data={"habit_id": habit_id, "is_done": True}
    )

    if number_completed == required_count:
        end_date = await TrackingRepository.get_end_date_habit(
            session=session, habit_id=habit_id
        )
        await end_habit(session=session, habit_id=habit_id, end_date=end_date)
        return True
    return False
