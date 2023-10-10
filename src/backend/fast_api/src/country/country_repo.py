from dataclasses import dataclass
from fastapi import Depends
from db.config import get_session, AsyncSession
from src.country.dto.country_dto import CountryDTO
from src.country.country_model import Country
from src.city.city_model import City
from src.state.state_model import State
from sqlalchemy import select, func
from typing import List


@dataclass
class CountryRepo:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db

    async def get_all_countries(self) -> List[CountryDTO]:
        pass

    async def get_num_existing_countries(self) -> int:
        num_countries = await self.db_session.execute(
            select(func.count()).select_from(Country)
        )
        return num_countries.scalar()

    async def add(self, country: CountryDTO) -> None:
        created_by = "SYSTEM"
        if country:
            ctry = Country(
                name=country.name,
                iso_2=country.iso_2,
                iso_3=country.iso_3,
                currency=country.currency,
                currency_name=country.currency_name,
                currency_symbol=country.currency_symbol,
                emoji_unicode=country.emoji_uncicode,
                phone_code=country.phone_code,
                latitude=country.location.latitude,
                longitude=country.location.longitude,
                created_by=created_by,
                states=[
                    State(
                        name=state.name,
                        code=state.code,
                        latitude=state.location.latitude,
                        longitude=state.location.longitude,
                        created_by=created_by,
                        cities=[
                            City(
                                name=city.name,
                                latitude=city.location.latitude,
                                longitude=city.location.longitude,
                                created_by=created_by,
                            )
                            for city in state.cities
                        ],
                    )
                    for state in country.states
                ],
            )

            self.db_session.add(ctry)
            await self.db_session.commit()
            ctry = None
