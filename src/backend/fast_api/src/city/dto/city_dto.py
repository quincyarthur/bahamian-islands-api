from dataclasses import dataclass
from typing import Optional
from src.location.dto.location_dto import Location


@dataclass
class CityDTO:
    name: str
    location: Optional[Location]
