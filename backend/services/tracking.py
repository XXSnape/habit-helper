from sqlalchemy.ext.asyncio import AsyncSession

from repositories.tracking import TrackingRepository
from schemas.habits import MarkHabitSchema
from services.habits import end_habit
from utils.validations import check_date_format


async def mark_habit_by_id(
    session: AsyncSession, habit_id: int, mark: MarkHabitSchema
) -> bool:
    data = mark.model_dump(exclude_none=True)
    if "date" in data:
        data["date"] = check_date_format(data["date"])
    data["habit_id"] = habit_id
    tracking_id = await TrackingRepository.create_object(session=session, data=data)
    return bool(tracking_id)


async def is_habit_complete(session: AsyncSession, habit_id: int, required_count: int):
    number_completed = await TrackingRepository.count_number_objects_by_params(
        session=session, data={"habit_id": habit_id}
    )
    if number_completed == required_count:
        await end_habit(session=session, habit_id=habit_id)
        return True
    return False
