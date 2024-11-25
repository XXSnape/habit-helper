from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import HabitModel
from repositories.habits import HabitRepository
from schemas.habits import HabitCreateSchema


async def create_habit(
    session: AsyncSession, habit_in: HabitCreateSchema, user_id: int
) -> bool:
    data = habit_in.model_dump()
    data["user_id"] = user_id
    habit_id = await HabitRepository.create_object(session=session, data=data)
    return bool(habit_id)


async def get_number_completed(
    session: AsyncSession, habit_id: int, user_id: int
) -> int:
    required_count = await HabitRepository.get_required_count(
        session=session, data={"id": habit_id, "user_id": user_id}
    )
    if required_count is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The habit was not found",
        )
    return required_count


async def end_habit(session: AsyncSession, habit_id: int):
    await HabitRepository.update_object_by_params(
        session=session, filter_data={"id": habit_id}, update_data={"is_done": True}
    )


async def mark_habit_by_id(session: AsyncSession, habit_id: int):
    pass
