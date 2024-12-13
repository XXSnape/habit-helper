from sqlalchemy.ext.asyncio import AsyncSession

from repositories.habits import HabitRepository
from repositories.tracking import TrackingRepository
from schemas.habits import MarkHabitSchema
from services.habits import end_habit, habit_not_exists
from utils.validations import check_date_format


async def mark_habit_by_id(
    session: AsyncSession, habit_id: int, mark: MarkHabitSchema
) -> bool:
    data = mark.model_dump(exclude_none=True)
    data["date"] = check_date_format(data["date"])
    data["habit_id"] = habit_id
    tracking_id = await TrackingRepository.create_object(session=session, data=data)
    return bool(tracking_id)


async def is_habit_complete(
    session: AsyncSession, habit_id: int, required_count: int
) -> bool:
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


async def change_habit_reason_by_id(
    session: AsyncSession, habit_id: int, user_id: int, date: str, new_reason: str
) -> bool:
    if not HabitRepository.get_object_id_by_params(
        session=session, data={"id": habit_id, "user_id": user_id}
    ):
        raise habit_not_exists
    result = await TrackingRepository.update_object_by_params(
        session=session,
        filter_data={"habit_id": habit_id, "date": check_date_format(date)},
        update_data={"reason": new_reason},
    )
    if not result:
        raise habit_not_exists
    return result
