from typing import Optional

from utils.enums import MarketType, StoreType


class StoreParamsDTO:

    name: Optional[str]
    platform_id: Optional[str]
    market_type: Optional[MarketType]
    store_type: Optional[StoreType]

    def __init__(
        self,
        name: Optional[str] = None,
        platform_id: Optional[str] = None,
        market_type: Optional[MarketType] = None,
        store_type: Optional[StoreType] = None,
    ) -> None:
        self.store_type = store_type
        self.market_type = market_type
        self.name = name
        self.platform_id = platform_id

    def __repr__(self) -> str:
        return f'''
            StoreParamsDTO <name: {self.name}, platform_id: {self.platform_id}, market_type: {self.market_type}, store_type: {self.store_type}>
        '''
