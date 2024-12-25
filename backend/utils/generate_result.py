from schemas.results import ResultSchema

from .exceptions import habit_not_exists


def get_result_for_request(result: bool) -> ResultSchema:
    """
    Если результат действия операции result равен False, вызывается исключение
    :param result: результат операции
    :return: ResultSchema
    """
    if result is False:
        raise habit_not_exists
    return ResultSchema(result=result)
