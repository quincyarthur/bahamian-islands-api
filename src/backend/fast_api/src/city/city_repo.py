from dataclasses import dataclass
from fastapi import Depends
from db.config import get_session, AsyncSession
from src.city.dto.city_dto import CityDTO
from src.city.city_model import City
from src.location.dto.location_dto import Location
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from src.state.state_model import State


@dataclass
class CityRepo:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db

    async def get_cities_by_state(self, state_name: str) -> List[CityDTO]:
        stmt = (
            select(City)
            .join(City.state)
            .where(State.name == state_name)
            .options(contains_eager(City.state))
        )
        results = await self.db_session.execute(stmt)
        cities = results.scalars().all()
        return [self.to_city_dto(city=city) for city in cities]

    def to_city_dto(self, city: City) -> CityDTO | None:
        city_dto: CityDTO = None
        if city:
            city_dto = CityDTO(
                name=city.name,
                location=Location(latitude=city.latitude, longitude=city.longitude),
            )
        return city_dto
