from functools import reduce
from typing import Optional
from sqlmodel import func, select

from models.ecommerce import EcommercePlatform, EcommercePlatformSignature
from models._database import SessionDep
from schemas.ecommerce import PlatformCreate, PlatformSignatureCreate
from utils.exceptions import InvalidInputException
from utils.enums import FingerprintType


class PlatformService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session

    async def _check_exists(self, name: str) -> bool:
        return bool(self._session.scalar(
            select(EcommercePlatform).where(func.lower(EcommercePlatform.name) == name)
        ))

    async def create(
        self, platformCreate: PlatformCreate
    ) -> tuple[Optional[EcommercePlatform], dict[str, str]]:
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
    
    async def get_by_id(self, platform_id: str) -> Optional[EcommercePlatform]:
        return self._session.get(EcommercePlatform, platform_id)

    async def get_list(self) -> list[EcommercePlatform]:
        return list(
            self._session.scalars(
                select(EcommercePlatform).where(EcommercePlatform.is_active)
            ).all()
        )


class PlatformSignatureService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session
    
    async def create(
        self, platform_id: str, signatures: list[PlatformSignatureCreate]
    ) -> tuple[list[EcommercePlatformSignature], dict[str, str]]:
        platform_signatures: list[EcommercePlatformSignature] = []
        errors: dict[str, str] = {}
        try:
            for signature in signatures:
                platform_signature: Optional[EcommercePlatformSignature] = (
                    await self.get_by_platform_and_type(platform_id, signature.type)
                )
                if platform_signature is not None:
                    platform_signature.values = signature.values
                    platform_signature.confidence = (
                        signature.confidence 
                            if signature.confidence is not None 
                            else platform_signature.confidence
                    )
                    platform_signatures.append(platform_signature)
                else:
                    platform_signatures.append(EcommercePlatformSignature(signature, platform_id))
                
            self._session.add_all(platform_signatures)
            self._session.commit()
            for signature in platform_signatures: 
                self._session.refresh(signature)
        except Exception as ex:
            errors['general'] = reduce(lambda x, y: x + y,  ex.args, '')
        
        return platform_signatures, errors

    async def get_by_platform(self, platform_id: str) -> list[EcommercePlatformSignature]:
        return list(
            self._session.scalars(
                select(EcommercePlatformSignature)
                .where(EcommercePlatformSignature.platform_id == platform_id)
            )
        )
    
    async def get_by_platform_and_type(
        self, platform_id: str, type: FingerprintType
    ) -> Optional[EcommercePlatformSignature]:
        return self ._session.scalar(
            select(EcommercePlatformSignature).where(
                EcommercePlatformSignature.platform_id == platform_id,
                EcommercePlatformSignature.type == type,
            )
        )
    