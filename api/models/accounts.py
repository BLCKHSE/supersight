from datetime import datetime
from typing import Optional
from sqlmodel import TIMESTAMP, Column, Field, SQLModel, String

from schemas.accounts import AccountCreate
from utils.helpers import GeneralHelper

class UserAccount(SQLModel, table=True):

    __tablename__ = 'accounts' # type: ignore

    created_on: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False),
        allow_mutation=False
    )
    credits: float = Field(default=0)
    email: str = Field(nullable=False, unique=True, max_length=60)
    first_name: str = Field(nullable=False, max_length=30, min_length=3)
    home_ip_address: Optional[str] = Field(sa_column=Column(String), regex='^([0-9]{1,3}\\.?){4}$')
    id: str = Field(sa_column=Column(String,  default=GeneralHelper.get_ulid, primary_key=True), max_length=26)
    last_name: Optional[str] = Field(nullable=True, max_length=30, min_length=1)
    password_hash: str = Field(sa_column=Column(String), max_length=300)

    def __init__(self, accountCreate: AccountCreate):
        self.email = accountCreate.email
        self.first_name = accountCreate.first_name
        self.home_ip_address = accountCreate.home_ip_address
        self.last_name = accountCreate.last_name


    @property
    def full_name(self) -> str:
        return self.first_name + (f' {self.last_name}' if self.last_name else '')
