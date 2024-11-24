from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    telegram_id: int


class UserCreate(UserSchema):
    pass
