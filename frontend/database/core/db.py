import functools
from typing import Callable

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.db.url, echo=settings.db.echo)
session_factory = sessionmaker(bind=engine)


class GetSession[T, **P]:
    """
    Декорирует функцию, добавляя в ее аргументы сессию для работы с базой данных
    """

    def __init__(self, func: Callable[P, T]) -> None:
        """
        Инициализация

        :param func: функция, работающая с базой данных
        """
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """
        Подставляет в аргументы функции self.func
        аргумент session с открытой сессией для работы с базой данных
        :return: результат декорируемой функции
        """
        with session_factory() as session:
            result = self.func(*args, **kwargs, session=session)
        return result
