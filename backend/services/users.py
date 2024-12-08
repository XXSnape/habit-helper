from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel
from schemas.users import (
    UserCreate,
    UserSchema,
    UserHabitSchema,
    UserOutput,
    UserActivitySchema,
)
from repositories.users import UserRepository
from utils.auth import hash_password, validate_password

from schemas.users import UserChangeTelegramIdSchema, UserChangePassword

from utils.auth import get_access_token


async def create_user(session: AsyncSession, user_in: UserCreate) -> int:
    data = user_in.model_dump()
    hash_psw = hash_password(user_in.password)
    data["password"] = hash_psw
    return await UserRepository.create_object(session=session, data=data)


async def verify_existence_user(session: AsyncSession, user_in: UserSchema) -> int:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid telegram_id",
    )
    user_id: int | None = await UserRepository.get_object_id_by_params(
        session=session, data={"telegram_id": user_in.telegram_id}
    )
    if user_id is None:
        raise unauthed_exc
    return user_id


async def get_users_habits_by_hour(
    session: AsyncSession, hour: int
) -> list[UserHabitSchema]:
    users_and_habits = await UserRepository.get_users_habits_by_hour(
        session=session, hour=hour
    )
    return [
        UserHabitSchema.model_validate(user_and_habit, from_attributes=True)
        for user_and_habit in users_and_habits
    ]


async def verify_username(session: AsyncSession, username: str) -> bool:
    result = await UserRepository.get_object_id_by_params(
        session=session, data={"username": username}
    )
    return bool(result)


async def change_telegram_id_by_credentials(
    session: AsyncSession, user_in: UserChangeTelegramIdSchema
) -> tuple[int, int]:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user: UserModel | None = await UserRepository.get_object_by_params(
        session=session,
        data={
            "username": user_in.username,
        },
    )
    if (
        user is None
        or validate_password(password=user_in.password, hashed_password=user.password)
        is False
    ):
        raise unauthed_exc
    last_telegram_id = user.telegram_id
    user_id = user.id
    await UserRepository.update_object_by_params(
        session=session,
        filter_data={"id": user.id},
        update_data={"telegram_id": user_in.telegram_id},
    )
    return last_telegram_id, user_id


async def change_password_by_user_id(
    session: AsyncSession, user_in: UserChangePassword, user_id: int
) -> str:
    new_hash_password = hash_password(user_in.password)
    result = await UserRepository.update_object_by_params(
        session=session,
        filter_data={"id": user_id},
        update_data={"password": new_hash_password},
    )
    if result:
        return get_access_token(user_id=user_id)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def get_user_info_by_id(session: AsyncSession, user_id: int) -> UserOutput:
    user_data = await UserRepository.get_user_info(session=session, user_id=user_id)
    return UserOutput.model_validate(user_data, from_attributes=True)


async def activate_or_deactivate_user(
    session: AsyncSession, user_in: UserActivitySchema, user_id: int
) -> bool:
    return await UserRepository.update_object_by_params(
        session=session,
        filter_data={"id": user_id},
        update_data={"is_active": user_in.is_active},
    )
