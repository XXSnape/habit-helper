from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from core.helper import db_helper
from schemas.results import ResultSchema
from schemas.tokens import TokenSchema, TgIdAndTokenSchema
from schemas.users import (
    UserCreate,
    UserSchema,
    UserChangePassword,
    UserOutput,
    UserChangeTelegramIdSchema,
    UserActivitySchema,
)
from services.users import (
    verify_username,
    create_user,
    verify_existence_user,
    change_telegram_id_by_credentials,
    change_password_by_user_id,
    get_user_info_by_id,
    activate_or_deactivate_user,
)
from utils.auth import get_access_token
from dependencies.auth import get_user_id


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/", response_model=UserOutput)
async def get_my_info(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    return await get_user_info_by_id(session=session, user_id=user_id)


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


@router.patch("/change_telegram_id/", response_model=TgIdAndTokenSchema)
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


@router.patch("/change_password/", response_model=TokenSchema)
async def change_password(
    user_password: UserChangePassword,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    token = await change_password_by_user_id(
        session=session, user_in=user_password, user_id=user_id
    )
    return TokenSchema(access_token=token)


@router.patch("/change_activity/")
async def change_user_activity(
    user_activity: UserActivitySchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    user_id: Annotated[int, Depends(get_user_id)],
):
    result = await activate_or_deactivate_user(
        session=session, user_in=user_activity, user_id=user_id
    )
    return ResultSchema(result=result)
