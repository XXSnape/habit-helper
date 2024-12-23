class InvalidAccessToken(Exception):
    """
    Исключение, возникающее при ошибке авторизации
    """

    pass


class InvalidApiResponse(Exception):
    """
    Исключение, возникающее, когда бэкэнд прислал статус
    с ошибками сервера или пользователя
    """

    def __init__(self, message: str = "") -> None:
        """
        Инициализация
        :param message: сообщение для передачи в сплывающее окно пользователю
        """
        self.message = message

    def __str__(self) -> str:
        """
        :return: self.message
        """
        return self.message


class TokenMissing(Exception):
    """
    Исключение, возникающее, если в базе нет токена пользователя
    """

    pass
