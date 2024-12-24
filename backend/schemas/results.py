from pydantic import BaseModel


class ResultSchema(BaseModel):
    """
    Схема для представления результата операции

    result - True, если операция прошла успешно, иначе False
    """

    result: bool
