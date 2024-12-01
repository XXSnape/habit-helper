from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel
from schemas.users import UserCreate, UserSchema, UserHabitSchema
from repositories.users import UserRepository
from utils.auth import hash_password, validate_password


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
