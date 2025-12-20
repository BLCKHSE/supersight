from typing import Annotated, Optional
from fastapi import APIRouter, Depends

from models.ecommerce import EcommercePlatform, EcommercePlatformSignature
from schemas.ecommerce import PlatformCreate, PlatformSignatureCreate
from services.ecommerce import PlatformService, PlatformSignatureService
from utils.exceptions import InvalidInputException


ecommRouter: APIRouter = APIRouter()

@ecommRouter.post(path='/platforms')
async def add(
    platformCreate: PlatformCreate,
    platform_service: Annotated[PlatformService, Depends()],
):
    
    platform, errors = await platform_service.create(platformCreate)
    if errors:
        raise InvalidInputException(errors['platform'])
    if platform:
        return platform.model_dump(mode='json', include={'id', 'name', 'logo_url', 'url'})


@ecommRouter.get(path='/platforms')
async def get_list(
    platform_service: Annotated[PlatformService, Depends()]
):
    platforms: list[EcommercePlatform] = await platform_service.get_list()
    return platforms


@ecommRouter.post(path='/platforms/{platform_id}/signatures', response_model=list[EcommercePlatformSignature])
async def add_or_update_signatures(
    signatures: list[PlatformSignatureCreate],
    platform_id: str,
    platform_service: Annotated[PlatformService, Depends()],
    platform_signature_service: Annotated[PlatformSignatureService, Depends()],
):
    platform: Optional[EcommercePlatform] = await platform_service.get_by_id(platform_id)
    if platform is None:
        raise InvalidInputException('platform_id', 'not found')
    
    platform_signatures, errors = await platform_signature_service.create(platform_id, signatures)

    if errors:
        raise InvalidInputException(errors['general'])
    
    return platform_signatures


@ecommRouter.get(path='/platforms/{platform_id}/signatures', response_model=list[EcommercePlatformSignature])
async def get_signatures(
    platform_id: str,
    platform_signature_service: Annotated[PlatformSignatureService, Depends()],
) -> list[EcommercePlatformSignature]:
    return await platform_signature_service.get_by_platform(platform_id)
