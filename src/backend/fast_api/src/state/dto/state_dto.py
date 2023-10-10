from dataclasses import dataclass, field
from typing import Optional, List
from src.location.dto.location_dto import Location
from src.city.dto.city_dto import CityDTO


@dataclass
class StateDTO:
    name: str
    code: Optional[str]
    location: Optional[Location]
    cities: Optional[List[CityDTO]] = field(default_factory=list)
