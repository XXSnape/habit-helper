from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import get_user_id
from core.helper import db_helper
from schemas.habits import (
    HabitCreateSchema,
    MarkHabitSchema,
    HabitCompletedSchema,
    HabitPatchSchema,
    HabitResumeSchema,
    HabitOutputSchema,
    ReasonChangeSchema,
    HabitNameSchema,
)
from schemas.results import ResultSchema
from schemas.users import UserHabitSchema
from services.habits import (
    create_habit,
    get_number_completed,
    delete_habit_by_id,
    patch_habit_by_id,
    resume_habit_by_id,
    get_habits_by_id,
    get_habit_name_by_id,
)
from services.tracking import (
    mark_habit_by_id,
    is_habit_complete,
    change_habit_reason_by_id,
)
from services.users import get_users_habits_by_hour

from utils.generate_result import get_result_for_request

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
    if not habit_created:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The habit was not created",
        )
    return ResultSchema(result=habit_created)


@router.patch(
    "/{habit_id}/", status_code=status.HTTP_200_OK, response_model=ResultSchema
)
async def patch_habit(
    habit_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    updated_habit: HabitPatchSchema,
    user_id: Annotated[int, Depends(get_user_id)],
):
    result = await patch_habit_by_id(
        session=session, habit_id=habit_id, user_id=user_id, habit_in=updated_habit
    )
    return get_result_for_request(result)


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
    if tracking is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The habit has already been noted",
        )
    habit_completed = await is_habit_complete(
        session=session, habit_id=habit_id, required_count=number_completed
    )
    return HabitCompletedSchema(result=tracking, completed=habit_completed)


@router.delete(
    "/{habit_id}/", status_code=status.HTTP_200_OK, response_model=ResultSchema
)
async def delete_habit(
    habit_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    result = await delete_habit_by_id(
        session=session, habit_id=habit_id, user_id=user_id
    )
    return get_result_for_request(result)


@router.patch(
    "/resume/{habit_id}", status_code=status.HTTP_200_OK, response_model=ResultSchema
)
async def resume_habit(
    habit_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
    habit_resume: HabitResumeSchema,
):
    result = await resume_habit_by_id(
        session=session,
        habit_id=habit_id,
        user_id=user_id,
        new_count=habit_resume.count,
    )
    return get_result_for_request(result)


@router.get(
    "/me/", status_code=status.HTTP_200_OK, response_model=list[HabitOutputSchema]
)
async def get_my_habits(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
    is_complete_null: bool = True,
):
    habits = await get_habits_by_id(
        session=session,
        user_id=user_id,
        is_complete_null=is_complete_null,
    )
    return habits


@router.get("/", response_model=list[UserHabitSchema])
async def get_users_habits(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    notification_hour: int,
):
    result = await get_users_habits_by_hour(session=session, hour=notification_hour)
    return result


@router.get("/{habit_id}/", response_model=HabitNameSchema)
async def get_habit_name(
    habit_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    return await get_habit_name_by_id(
        session=session, habit_id=habit_id, user_id=user_id
    )
