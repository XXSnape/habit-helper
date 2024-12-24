from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Схема для представления информации о телеграм id пользователя

    telegram_id - телеграм id
    """

    telegram_id: int


class UserCreate(UserSchema):
    """
    Схема для создания пользователя

    username - имя
    password - пароль
    """

    username: str
    password: str


class UserHabitSchema(UserSchema):
    """
    Схема с информацией о пользователе и названия привычки

    id - id привычки
    name - название привычки
    """

    id: int
    name: str


class UserChangeTelegramIdSchema(UserCreate):
    """
    Схема с информацией о новом telegram id

    telegram_id - телеграм id
    """

    telegram_id: int


class UserChangePassword(BaseModel):
    """
    Схема для смены пароля пользователя
    password - обновлённый пароль
    """

    password: str


class UserOutput(BaseModel):
    """
    Схема с информацией о пользователе

    username - имя
    is_active - статус активности
    date_of_registration - дата и время регистрации
    """

    username: str
    is_active: bool
    date_of_registration: datetime


class UserActivitySchema(BaseModel):
    """
    Схема с информацией о том, активен ли пользователь
    is_active - статус активности. Если True, пользователю приходят напоминания,
    если False, то не приходят
    """
    is_active: bool
