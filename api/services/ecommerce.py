from functools import reduce
from typing import Optional
from sqlmodel import func, select

from models.ecommerce import EcommercePlatform, EcommercePlatformSignature
from models._database import SessionDep
from schemas.ecommerce import PlatformCreate
from utils.exceptions import InvalidInputException


class PlatformService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session

    async def _check_exists(self, name: str) -> bool:
        return bool(self._session.scalar(
            select(EcommercePlatform).where(func.lower(EcommercePlatform.name) == name)
        ))

    async def create(self, platformCreate: PlatformCreate) -> tuple[Optional[EcommercePlatform], dict[str, str]]:
        platform: Optional[EcommercePlatform] = None
        errors: dict[str, str] = {}
        if (await self._check_exists(platformCreate.name)):
            raise InvalidInputException('name', 'already in use')
        try:
            platform = EcommercePlatform(platformCreate)
            self._session.add(platform)
            self._session.commit()
            self._session.refresh(platform)
        except Exception as ex:
            errors['platform'] = reduce(lambda x, y: x + y,  ex.args, '')
        
        return platform, errors

    async def get_list(self) -> list[EcommercePlatform]:
        return list(
            self._session.scalars(
                select(EcommercePlatform).where(EcommercePlatform.is_active)
            ).all()
        )


class PlatformSignatureService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session

    async def get_by_platform(self, platform_id: str) -> list[EcommercePlatformSignature]:
        return list(
            self._session.scalars(
                select(EcommercePlatformSignature)
                .where(EcommercePlatformSignature.platform_id == platform_id)
            )
        )
    