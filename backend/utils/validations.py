from datetime import date, datetime

from fastapi import HTTPException, status


def check_date_format(date_in: str) -> date:
    """
    Проверяет переданный формат даты. Если он некорректен, вызывается исключение
    :param date_in: дата
    :return:
    """
    try:
        return datetime.strptime(date_in, "%Y%m%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The date is not in the yyyy-MM-dd format",
        )
