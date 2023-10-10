from dataclasses import dataclass
from fastapi import Depends
from db.config import get_session, AsyncSession
from typing import List
from src.state.dto.state_dto import StateDTO
from src.state.state_model import State
from src.country.country_model import Country
from src.location.dto.location_dto import Location
from sqlalchemy import select
from sqlalchemy.orm import contains_eager, lazyload
from src.city.city_repo import CityRepo
from src.city.city_model import City


@dataclass
class StateRepo:
    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
        city_repo: CityRepo = Depends(CityRepo),
    ) -> None:
        self.db_session = db
        self.city_repo = city_repo

    async def get_states_by_country(
        self, country_name: str, include_cities: bool
    ) -> List[StateDTO]:
        stmt = (
            select(State)
            .join(State.country)
            .join(State.cities)
            .where(Country.name == country_name)
            .options(contains_eager(State.cities))
        )
        results = await self.db_session.execute(stmt)
        states = results.scalars().unique()
        return [
            await self.to_state_dto(state=state, include_cities=include_cities)
            for state in states
        ]

    async def to_state_dto(
        self, state: State, include_cities: bool = False
    ) -> StateDTO | None:
        state_dto: StateDTO = None
        if state:
            state_dto = StateDTO(
                name=state.name,
                code=state.code,
                location=Location(latitude=state.latitude, longitude=state.longitude),
                cities=[self.city_repo.to_city_dto(city=city) for city in state.cities]
                if include_cities
                else [],
            )
        return state_dto
