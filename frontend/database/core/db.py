from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.db.url, echo=settings.db.echo)
session_factory = sessionmaker(bind=engine)


class GetSession:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        with session_factory() as session:
            result = self.func(*args, **kwargs, session=session)
        return result
