from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.habits import HabitRepository
from schemas.habits import (
    HabitCreateSchema,
    HabitPatchSchema,
    HabitOutputSchema,
    HabitNameSchema,
)

from utils.exceptions import habit_not_exists


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
        session=session, data={"id": habit_id, "user_id": user_id, "completed_at": None}
    )
    if required_count is None:
        raise habit_not_exists
    return required_count


async def end_habit(session: AsyncSession, habit_id: int, end_date: date) -> None:
    await HabitRepository.update_object_by_params(
        session=session,
        filter_data={"id": habit_id},
        update_data={"completed_at": end_date},
    )


async def delete_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int
) -> bool:
    result = await HabitRepository.delete_object_by_params(
        session=session, data={"id": habit_id, "user_id": user_id}
    )
    if not result:
        raise habit_not_exists
    return result


async def patch_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int, habit_in: HabitPatchSchema
):
    data = habit_in.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No data available"
        )
    result = await HabitRepository.update_object_by_params(
        session=session,
        filter_data={"id": habit_id, "user_id": user_id},
        update_data=data,
    )
    if not result:
        raise habit_not_exists
    return result


async def resume_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int, new_count: int
) -> bool:
    filter_data = {"id": habit_id, "user_id": user_id}
    prev_count = await HabitRepository.get_required_count(
        session=session, data=filter_data
    )
    if new_count <= prev_count:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The new number of repetitions is less than or equal to the previous one",
        )
    return await HabitRepository.update_object_by_params(
        session=session,
        filter_data=filter_data,
        update_data={"count": new_count, "completed_at": None},
    )


async def get_habits_by_id(
    session: AsyncSession,
    user_id: int,
    is_complete_null: bool = True,
) -> list[HabitOutputSchema]:
    habits = await HabitRepository.get_habits(
        session=session,
        user_id=user_id,
        is_complete_null=is_complete_null,
    )
    return [
        HabitOutputSchema.model_validate(habit, from_attributes=True)
        for habit in habits
    ]


async def get_habit_name_by_id(
    session: AsyncSession, user_id: int, habit_id: int
) -> HabitNameSchema:
    name = await HabitRepository.get_habit_name(
        session=session, data={"id": habit_id, "user_id": user_id}
    )
    if not name:
        raise habit_not_exists
    return HabitNameSchema(name=name)
