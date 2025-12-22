from functools import reduce
from typing import Optional
from sqlmodel import func, or_, select

from dtos.ecommerce import StoreParamsDTO
from models.ecommerce import EcommercePlatform, EcommercePlatformSignature, EcommerceStore
from models._database import SessionDep
from schemas.ecommerce import PlatformCreate, PlatformSignatureCreate, StoreCreate
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


class StoreService:

    def __init__(self, session: SessionDep) -> None:
        self._session = session
        self._platform_service = PlatformService(session)

    async def _check_exists(self, name: str, domain_name: str) -> list[str]:
        invalid_fields: list[str] = []
        stores: list[EcommerceStore] =  list(self._session.scalars(
            select(EcommerceStore)
                .where(or_(
                    func.lower(EcommerceStore.name) == name.lower(),
                    func.lower(EcommerceStore.domain_name) == domain_name.lower(),
                ))
        ).all())

        for store in stores:
            if store.name.lower() == name.lower():
                invalid_fields.append('name')
            elif store.domain_name.lower() == domain_name.lower():
                invalid_fields.append('domainName')

        return invalid_fields
    
    async def create(
        self, storeCreate: StoreCreate
    ) -> tuple[Optional[EcommerceStore], dict[str, str]]:
        
        store: Optional[EcommerceStore] = None
        errors: dict[str, str] = {}
        if storeCreate.platform_id:
            platform: Optional[EcommercePlatform] = await self._platform_service.get_by_id(storeCreate.platform_id)
            if platform is None:
                raise InvalidInputException('platform_id', 'not found')
        
        invalid_fields = await self._check_exists(storeCreate.name, storeCreate.domain_name)
        if len(invalid_fields) > 0:
            raise InvalidInputException(invalid_fields[0], 'already in use')
        try:
            store = EcommerceStore(storeCreate)
            self._session.add(store)
            self._session.commit()
            self._session.refresh(store)
        except Exception as ex:
            errors['store'] = reduce(lambda x, y: x + y,  ex.args, '')

        return store, errors
    
    async def get_by_id(self, store_id: str) -> Optional[EcommerceStore]:
        return self._session.get(EcommerceStore, store_id)
    
    async def get_list(self, params: StoreParamsDTO) -> list[EcommerceStore]:
        stmt = select(EcommerceStore)
        
        if params.name:
            stmt = stmt.where(or_(EcommerceStore.name.ilike(f'%{params.name}%'))) # type: ignore
        if params.platform_id:
            stmt = stmt.where(or_(EcommerceStore.platform_id == params.platform_id))
        if params.market_type:
            stmt = stmt.where(or_(EcommerceStore.market_type == params.market_type))
        if params.store_type:
            stmt = stmt.where(or_(EcommerceStore.store_type == params.store_type))

        return list(self._session.exec(stmt.order_by(EcommerceStore.updated_on.desc()))) # type: ignore
