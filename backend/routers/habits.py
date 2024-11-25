from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import get_user_id
from core.helper import db_helper
from schemas.habits import HabitCreateSchema, MarkHabitSchema, HabitCompletedSchema
from schemas.results import ResultSchema
from services.habits import create_habit, get_number_completed
from services.tracking import mark_habit_by_id, is_habit_complete

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResultSchema)
async def create_new_habit(
    habit: HabitCreateSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    habit_created = await create_habit(session=session, habit_in=habit, user_id=user_id)
    return ResultSchema(result=habit_created)


@router.post(
    "/mark/{habit_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=HabitCompletedSchema,
)
async def mark_habit(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    habit_id: int,
    mark: MarkHabitSchema,
    user_id: Annotated[int, Depends(get_user_id)],
):
    number_completed = await get_number_completed(
        session=session, habit_id=habit_id, user_id=user_id
    )
    tracking = await mark_habit_by_id(session=session, habit_id=habit_id, mark=mark)
    habit_completed = False
    if tracking:
        habit_completed = await is_habit_complete(
            session=session, habit_id=habit_id, required_count=number_completed
        )
    return HabitCompletedSchema(result=tracking, completed=habit_completed)
