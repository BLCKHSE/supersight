from re import match
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AccountCreate(BaseModel):

    first_name: str = Field(serialization_alias='firstName', max_length=30, min_length=3)
    last_name: Optional[str] = Field(serialization_alias='lastName',default=None, max_length=30, min_length=1)
    email: str = Field(max_length=60)
    home_ip_address: Optional[str] = Field(serialization_alias='homeIpAddress',default=None, pattern='^([0-9]{1,3}\\.?){4}$')
    password: Optional[str]

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value: str):
        password_pattern: str = (
            '^(?P<a>(?=.*[0-9]+)(?=.*[a-z]+)(?=.*[A-Z]+)(?=.*[\\.\\?_\\-\\*\\(\\)\\+\\$&=%\\#@!]+)).{6,15}$'
        )
        if value and not match(password_pattern, value):
            raise ValueError(
                'must be between 6-15 chars long and contian at least 1 capiatl char, & 1 special char($,&,=,_,-)'
            )
