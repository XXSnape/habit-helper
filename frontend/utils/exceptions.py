class InvalidAccessToken(Exception):
    pass


class InvalidApiResponse(Exception):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message
