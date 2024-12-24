from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Схема для представления токена пользователя

    access_token - временный токен доступа
    token_type - тип токена
    """

    access_token: str
    token_type: str = "Bearer"


class TgIdAndTokenSchema(TokenSchema):
    """
    Схема для представления информации о новом телеграм id и токене временного доступа

    telegram_id - изменённый телеграм id
    """

    telegram_id: int
