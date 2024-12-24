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
) -> ResultSchema:
    """
    Роутер для создания привычки
    :param habit: HabitCreateSchema
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return: ResultSchema
    """
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
) -> ResultSchema:
    """
    Роутер для обновления привычки
    :param habit_id: id привычки
    :param session: сессия для работы с базой
    :param updated_habit: HabitPatchSchema
    :param user_id: id пользователя
    :return:
    """
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
) -> HabitCompletedSchema:
    """
    Роутер для пометки привычки как выполненную или невыполненную.
    :param session: Сессия для работы с базой
    :param habit_id: id привычки
    :param mark: MarkHabitSchema
    :param user_id: id пользователя
    :return: HabitCompletedSchema
    """
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
) -> ResultSchema:
    """
    Роутер для удаления привычки
    :param habit_id: id привычки
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return: ResultSchema
    """
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
) -> ResultSchema:
    """
    Роутер для возобновления выполненной привычки
    :param habit_id: id привычки
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param habit_resume: HabitResumeSchema
    :return: ResultSchema
    """
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
) -> list[HabitOutputSchema]:
    """
    Роутер для получения привычек пользователя
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param is_complete_null: True, если нужны действующие привычки, иначе завершенные, False
    :return: list[HabitOutputSchema]
    """
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
) -> list[UserHabitSchema]:
    """
    Роутер для получения привычек пользователей,
    которые установили время напоминания о них на notification_hour часов
    :param session: сессия для работы с базой
    :param notification_hour: час напоминания
    :return: list[UserHabitSchema]
    """
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
) -> HabitNameSchema:
    """
    Роутер для получения названия привычки
    :param habit_id: id привычки
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return: HabitNameSchema
    """
    return await get_habit_name_by_id(
        session=session, habit_id=habit_id, user_id=user_id
    )
