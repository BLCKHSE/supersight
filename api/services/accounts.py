from functools import reduce
from typing import Optional

from sqlmodel import select

from models._database import SessionDep
from models.accounts import UserAccount
from schemas.accounts import AccountCreate


class AccountService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session

    async def create(self, accountDTO: AccountCreate) -> tuple[Optional[UserAccount], dict[str, str]]:
        userAccount: Optional[UserAccount] = None
        errors: dict[str, str] = {}
        try:
            userAccount = UserAccount(accountDTO)
            self._session.add(userAccount)
            self._session.commit()
            self._session.refresh(userAccount)
        except Exception as ex:
            errors['account'] = reduce(lambda x, y: x + y,  ex.args, '')
        
        return userAccount, errors

    async def get_by_email(self, email: str) -> Optional[UserAccount]:
        return self._session.scalars(
            select(UserAccount).filter_by(email=email)).one_or_none()
    
    async def get_by_id(self, id: str) -> Optional[UserAccount]:
        return self._session.get(UserAccount, id)
    