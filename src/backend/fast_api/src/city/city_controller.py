from fastapi import APIRouter, Depends, HTTPException, status
from src.city.dto.city_dto import CityDTO
from src.city.city_service import CityService
from typing import List, Union


router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


@router.get(
    "/",
    response_model=List[CityDTO],
    summary="Get Cities Within Island",
    description="Cities in most cases are settlements, however in cases like New Providence a city can be an area \
                i.e. Yamacraw, Killarney. A city can also be a surrounding island i.e. Spanish Wells within Eleuthera. \
                The cities definition is loose but the intent behind some of the categorization decisions is to allow \
                locals to naturally navigate the island/city mappings.",
)
async def get_cities(
    state_name: str,
    city_service: CityService = Depends(CityService),
):
    return await city_service.get_cities_by_state(state_name=state_name)
