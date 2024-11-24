from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.helper import db_helper
from schemas.tokens import TokenSchema
from schemas.users import UserCreate
from services.users import create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "register/", status_code=status.HTTP_201_CREATED, response_model=TokenSchema
)
async def register_user(
    user: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user_id = create_user(session=session, user_in=user)

