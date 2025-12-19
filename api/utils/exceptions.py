from typing import Optional


class InvalidInputException(Exception):

    field: str
    message: str

    def __init__(self, field: Optional[str] = None, message: Optional[str] = None) -> None:
        self.field = field if field is not None else 'general'
        self.message = message if message is not None else 'error found'
        super().__init__(self.message)
