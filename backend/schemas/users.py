from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int


class UserCreate(UserSchema):
    username: str
    password: str


class UserHabitSchema(UserSchema):
    id: int
    name: str
