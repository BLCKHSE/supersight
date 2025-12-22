from datetime import datetime
from typing import Optional
from sqlmodel import ARRAY, TIMESTAMP, Column, Enum, Field, Integer, Relationship, SQLModel, String, UniqueConstraint

from schemas.ecommerce import PlatformCreate, PlatformSignatureCreate, StoreCreate
from utils.enums import FingerprintType, MarketType, StoreType
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
        self.logo_url = platform.logo_url.unicode_string() if platform.logo_url else 'None'
        self.name = platform.name
        self.url = platform.url.unicode_string() if platform.url else 'None'


class EcommercePlatformSignature(SQLModel, table=True):

    __tablename__ = 'ecommerce_platform_signatures' # type: ignore
    __table_args__ = (
        UniqueConstraint("type", "platform_id", name="type_platform_id_constraint"),
    )

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


class EcommerceStore(SQLModel, table=True):

    __tablename__ = 'ecommerce_stores' # type: ignore

    available_tlds: Optional[list[str]] = Field(sa_column=Column(ARRAY(String)), max_length=20)
    created_on: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False),
    )
    description: Optional[str] = Field(max_length=150)
    domain_name: str = Field(unique=True, max_length=60, min_length=3)
    id: str = Field(sa_column=Column(
        String,  default=GeneralHelper.get_ulid, primary_key=True), max_length=26)
    logo_url: Optional[str] = Field(nullable=True, max_length=250)
    market_type: MarketType = Field(
        sa_column=Column(
            Enum(MarketType, name='market_type'),
            nullable=False,
            default=MarketType.B2C
        )
    )
    name: str = Field(unique=True, max_length=30, min_length=3)
    platform_id: Optional[str] = Field(foreign_key='ecommerce_platforms.id', nullable=True, ondelete='SET NULL')
    product_detail_uri_regex: Optional[str] = Field(max_length=250, nullable=True)
    store_type: StoreType = Field(
        sa_column=Column(
            Enum(StoreType, name='store_type'),
            nullable=False,
            default=StoreType.ONLINE_STORE
        )
    )
    updated_on: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False),
    )

    def __init__(self, store: StoreCreate):
        self.available_tlds = store.available_tlds
        self.description = store.description
        self.domain_name = store.domain_name
        self.logo_url = store.logo_url.unicode_string() if store.logo_url else 'None'
        self.market_type = store.market_type
        self.name = store.name
        self.platform_id = store.platform_id
        self.product_detail_uri_regex = store.product_detail_uri_regex
        self.store_type = store.store_type
