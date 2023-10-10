from fastapi import APIRouter, Depends, HTTPException, status
from src.state.dto.state_dto import StateDTO
from src.state.state_service import StateService
from typing import List


router = APIRouter(
    prefix="/states",
    tags=["states"],
)


@router.get(
    "/", response_model=List[StateDTO], summary="Get States/Islands Within Country"
)
async def get_states(
    country_name: str = "The Bahamas",
    state_service: StateService = Depends(StateService),
):
    return await state_service.get_states_by_country(country_name=country_name)
