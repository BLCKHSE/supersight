from re import match
from typing import Optional
from pydantic import BaseModel, field_validator
from sqlmodel import Field


class PlatformCreate(BaseModel):

    name: str = Field(max_length=30, min_length=3)
    url: Optional[str] = Field(default=None, max_length=250, nullable=True)
    logo_url: Optional[str] = Field(max_length=250, nullable=True, default=None)

    @field_validator('url', 'logo_url', mode='after')
    @classmethod
    def validate_password(cls, value: str):
        url_pattern: str = (
            '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'
        )
        if value and not match(url_pattern, value):
            raise ValueError(
                'must be a valid url'
            )
