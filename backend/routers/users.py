from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.schemas.users import UserChangeTelegramIdSchema
from backend.services.users import verify_username
from core.helper import db_helper
from schemas.results import ResultSchema
from schemas.tokens import TokenSchema, TgIdAndTokenSchema
from schemas.users import UserCreate, UserSchema
from services.users import (
    create_user,
    verify_existence_user,
    change_telegram_id_by_credentials,
)
from utils.auth import get_access_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=ResultSchema)
async def check_user_by_username(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.get_async_session)],
):
    result = await verify_username(session=session, username=username)
    return ResultSchema(result=result)


@router.post(
    "/register/", status_code=status.HTTP_201_CREATED, response_model=TokenSchema
)
async def register_user(
    user: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    user_id = await create_user(session=session, user_in=user)
    return TokenSchema(access_token=get_access_token(user_id=user_id))


@router.post("/new/", status_code=status.HTTP_201_CREATED, response_model=TokenSchema)
async def create_new_access_token(
    user: UserSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    user_id = await verify_existence_user(session=session, user_in=user)
    return TokenSchema(access_token=get_access_token(user_id=user_id))


@router.patch("/change_telegram_id/")
async def change_telegram_id(
    existing_user: UserChangeTelegramIdSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    last_telegram_id, user_id = await change_telegram_id_by_credentials(
        session=session, user_in=existing_user
    )
    access_token = get_access_token(user_id=user_id)
    return TgIdAndTokenSchema(access_token=access_token, telegram_id=last_telegram_id)
