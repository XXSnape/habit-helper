from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int


class UserCreate(UserSchema):
    username: str
    password: str
