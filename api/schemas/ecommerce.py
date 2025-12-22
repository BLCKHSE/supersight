from re import match
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from utils.enums import FingerprintType, MarketType, StoreType
from utils.validators import Url


class PlatformCreate(BaseModel):

    name: str = Field(max_length=30, min_length=3)
    url: Optional[Url] = Field(default=None, max_length=250)
    logo_url: Optional[Url] = Field(
        validation_alias='logoUrl', max_length=250, default=None)


class PlatformSignatureCreate(BaseModel):

    confidence: int = Field(ge=10, le=100)
    type: FingerprintType = Field()
    values: list[str] = Field(min_length=1, max_length=10)


class StoreCreate(BaseModel):

    available_tlds: Optional[list[str]] = Field(
        validation_alias='availableTlds', max_length=20, min_length=0)
    description: Optional[str] = Field(max_length=150)
    domain_name: str = Field(
        validation_alias='domainName', max_length=60, min_length=3)
    logo_url: Optional[Url] = Field(
        validation_alias='logoUrl', max_length=250)
    market_type: MarketType = Field(
        validation_alias='marketType', default=MarketType.B2C)
    name: str = Field(max_length=30, min_length=3)
    platform_id: Optional[str] = Field(validation_alias='platformId')
    product_detail_uri_regex: Optional[str] = Field(
        validation_alias='productDetialUriRegex', max_length=250)
    store_type: StoreType = Field(
        validation_alias='storeType', default=StoreType.ONLINE_STORE)

    @field_validator('available_tlds', mode='after')
    @classmethod
    def validate_tlds(cls, value: list[str]):
        tld_pattern: str = '(\\.[a-zA-Z]{2,6}){1,3}'
        invalid_tlds: list[str] = []
        for tld in value:
            if not match(tld_pattern, tld):
                invalid_tlds.append(tld)

        if len(invalid_tlds) > 0:
            raise ValueError(f'invalid TLDs found: {','.join(invalid_tlds)}')
