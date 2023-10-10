from dataclasses import dataclass
from fastapi import Depends
from db.config import get_session, AsyncSession
from typing import List
from src.state.dto.state_dto import StateDTO
from src.state.state_model import State
from src.country.country_model import Country
from src.location.dto.location_dto import Location
from sqlalchemy import select
from sqlalchemy.orm import contains_eager


@dataclass
class StateRepo:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db

    async def get_states_by_country(self, country_name: str) -> List[StateDTO]:
        stmt = (
            select(State)
            .join(State.country)
            .where(Country.name == country_name)
            .options(contains_eager(State.country))
        )
        results = await self.db_session.execute(stmt)
        states = results.scalars().all()
        return [self.to_state_dto(state=state) for state in states]

    def to_state_dto(self, state: State) -> StateDTO | None:
        state_dto: StateDTO = None
        if state:
            state_dto = StateDTO(
                name=state.name,
                code=state.code,
                location=Location(latitude=state.latitude, longitude=state.longitude),
            )
        return state_dto
