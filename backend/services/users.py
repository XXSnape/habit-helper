from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel
from schemas.users import UserCreate, UserSchema
from repositories.users import UserRepository
from utils.auth import hash_password, validate_password


async def create_user(session: AsyncSession, user_in: UserCreate) -> int:
    data = user_in.model_dump()
    hash_psw = hash_password(user_in.password)
    data["password"] = hash_psw
    return await UserRepository.create_object(session=session, data=data)


async def verify_existence_user(session: AsyncSession, user_in: UserSchema):
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
