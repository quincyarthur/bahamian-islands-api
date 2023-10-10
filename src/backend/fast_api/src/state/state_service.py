from dataclasses import dataclass
from src.state.dto.state_dto import StateDTO
from src.state.state_repo import StateRepo
from typing import List
from fastapi import HTTPException, status, Depends


@dataclass
class StateService:
    def __init__(self, state_repo: StateRepo = Depends(StateRepo)):
        self.state_repo = state_repo

    async def get_states_by_country(
        self, country_name: str, include_cities: bool
    ) -> List[StateDTO]:
        states = await self.state_repo.get_states_by_country(
            country_name=country_name, include_cities=include_cities
        )
        if not states:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return states
