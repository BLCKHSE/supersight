'''Accounts controllers module'''

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from models.accounts import UserAccount
from services.accounts import AccountService
from schemas.accounts import AccountCreate
from utils.exceptions import InvalidInputException


accountsRouter: APIRouter = APIRouter()

@accountsRouter.post('', status_code=status.HTTP_201_CREATED)
async def register(
    account: AccountCreate,
    account_service: Annotated[AccountService, Depends()]
):
    userAccount: Optional[UserAccount] = await account_service.get_by_email(account.email)

    if userAccount:
        raise InvalidInputException('email', 'already in use')
    
    userAccount, errors = await account_service.create(account)
    if userAccount:
        return userAccount.model_dump(mode='json', include={'id', 'email', 'created_on', 'full_name'})
    
    raise ValueError(errors['account'])


@accountsRouter.get('/{account_id}')
async def get_by_id(
    account_id: str,
    account_service: Annotated[AccountService, Depends()]
):

    userAccount: Optional[UserAccount] = await account_service.get_by_id(account_id)

    if not userAccount:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return userAccount.model_dump(mode='json', include={'id', 'email', 'created_on', 'full_name', 'credits'})
