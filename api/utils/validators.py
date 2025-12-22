from re import match
from typing import Annotated

from pydantic import AfterValidator, HttpUrl


def validate_url(value: HttpUrl):
    url_pattern: str = (
        '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{2,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'
    )
    if value and not match(url_pattern, value.unicode_string()):
        raise ValueError('must be a valid url')
    return value

Url = Annotated[HttpUrl, AfterValidator(validate_url)]
