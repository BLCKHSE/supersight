from typing import Optional
from sqlmodel import ARRAY, Column, Enum, Field, Integer, Relationship, SQLModel, String

from schemas.ecommerce import PlatformCreate, PlatformSignatureCreate
from utils.enums import FingerprintType
from utils.helpers import GeneralHelper


class EcommercePlatform(SQLModel, table=True):

    __tablename__ = 'ecommerce_platforms' # type: ignore

    id: str = Field(sa_column=Column(
        String,  default=GeneralHelper.get_ulid, primary_key=True), max_length=26)
    logo_url: Optional[str] = Field(nullable=True, max_length=250)
    name: str = Field(unique=True, max_length=30, min_length=3)
    url: Optional[str] = Field(max_length=250, nullable=True)
    is_active: bool = Field(default=True)

    signatures: list['EcommercePlatformSignature'] = Relationship(back_populates='platform', cascade_delete=True)

    def __init__(self, platform: PlatformCreate) -> None:
        self.logo_url = platform.logo_url
        self.name = platform.name
        self.url = platform.url


class EcommercePlatformSignature(SQLModel, table=True):

    __tablename__ = 'ecommerce_platform_signatures' # type: ignore

    confidence: int = Field(sa_column=Column(Integer, default=10), le=100, ge=10)
    id: str = Field(sa_column=Column(
        String,  default=GeneralHelper.get_ulid, primary_key=True), max_length=26)
    type: FingerprintType = Field(sa_column=Column(
        Enum(FingerprintType, name='fingerprint_type'), nullable=False))
    values: list[str] = Field(sa_column=Column(ARRAY(String)))
    platform_id: str = Field(foreign_key='ecommerce_platforms.id', nullable=False, ondelete='CASCADE')

    platform: EcommercePlatform = Relationship(back_populates='signatures')


    def __init__(self, signature: PlatformSignatureCreate, platform_id: str):

        self.type = signature.type
        self.confidence = signature.confidence
        self.platform_id = platform_id
        self.values = signature.values

