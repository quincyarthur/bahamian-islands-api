from dataclasses import dataclass
from typing import Optional, List
from src.location.dto.location_dto import Location
from src.state.dto.state_dto import StateDTO


@dataclass
class CountryDTO:
    name: str
    iso_2: str
    iso_3: str
    phone_code: str
    currency: str
    currency_name: str
    currency_symbol: str
    emoji_uncicode: str
    location: Optional[Location]
    states: Optional[List[StateDTO]]
