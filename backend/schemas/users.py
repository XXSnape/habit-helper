from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int


class UserCreate(UserSchema):
    username: str
    password: str


class UserHabitSchema(UserSchema):
    id: int
    name: str


class UserChangeTelegramIdSchema(UserCreate):
    telegram_id: int


class UserChangePassword(BaseModel):
    password: str


class UserOutput(BaseModel):
    username: str
    is_active: bool
    date_of_registration: datetime


class UserActivitySchema(BaseModel):
    is_active: bool
