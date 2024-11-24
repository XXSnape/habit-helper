from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserCreate
from repositories.users import UserRepository
from services.auth import hash_password


async def create_user(session: AsyncSession, user_in: UserCreate) -> int:
    data = user_in.model_dump()
    hash_psw = hash_password(user_in.password)
    data["password"] = hash_psw
    return await UserRepository.create_object(session=session, data=data)
