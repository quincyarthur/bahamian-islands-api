from dataclasses import dataclass
from src.city.city_repo import CityRepo
from src.city.dto.city_dto import CityDTO
from typing import List
from fastapi import HTTPException, status, Depends


@dataclass
class CityService:
    def __init__(self, city_repo: CityRepo = Depends(CityRepo)):
        self.city_repo = city_repo

    async def get_cities_by_state(
        self, state_name: str
    ) -> List[CityDTO] | HTTPException:
        cities = await self.city_repo.get_cities_by_state(state_name=state_name)
        if not cities:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return cities
