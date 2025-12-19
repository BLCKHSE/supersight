from typing import Annotated
from fastapi import APIRouter, Depends

from models.ecommerce import EcommercePlatform
from schemas.ecommerce import PlatformCreate
from services.ecommerce import PlatformService
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
