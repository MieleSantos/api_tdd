class BaseException(Exception):
    message: str = "Intenal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message: str = "Not Found"
