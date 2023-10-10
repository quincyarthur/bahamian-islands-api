import sys

sys.path.append("/usr/src/app")


from dataclasses import dataclass
from typing import List, Generator
import json
import os
from src.city.dto.city_dto import CityDTO
from src.state.dto.state_dto import StateDTO
from src.country.dto.country_dto import CountryDTO
from src.location.dto.location_dto import Location
from src.country.country_repo import CountryRepo
from db.config import async_session
import asyncio


def load_city(city: dict) -> CityDTO:
    city_dto: CityDTO = None
    if city:
        city_dto = CityDTO(
            name=city.get("name"),
            location=Location(
                latitude=city.get("latitude"), longitude=city.get("longitude")
            ),
        )
    return city_dto


def load_state(state: dict) -> StateDTO:
    state_dto: StateDTO = None
    if state:
        state_dto = StateDTO(
            name=state.get("name"),
            code=state.get("code"),
            location=Location(
                latitude=state.get("latitude"), longitude=state.get("longitude")
            ),
            cities=[load_city(city=city) for city in state.get("cities")],
        )
    return state_dto


def load_country(country: dict) -> CountryDTO:
    country_dto: CountryDTO = None
    if country:
        country_dto = CountryDTO(
            name=country.get("name"),
            iso_2=country.get("iso2"),
            iso_3=country.get("iso3"),
            phone_code=country.get("phone_code"),
            currency=country.get("currency"),
            currency_name=country.get("currency_name"),
            currency_symbol=country.get("currency_symbol"),
            emoji_uncicode=country.get("emojiU"),
            location=Location(
                latitude=country.get("latitude"), longitude=(country.get("longitude"))
            ),
            states=[load_state(state=state) for state in country.get("states")],
        )
    return country_dto


def get_countries(file_path: str) -> Generator[dict, None, None]:
    with open(file=file_path, mode="r") as file:
        data = json.loads(file.read())

    for country in data:
        yield country


def tables_empty():
    pass


async def seed_countries():
    async with async_session() as session:
        country_repo: CountryRepo = CountryRepo(db=session)
        existing_countries = await country_repo.get_num_existing_countries()

        if existing_countries:
            print("Countries found...terminating seeder")
            return

        data_directory = os.path.join(
            os.path.dirname(os.path.realpath(filename=__file__)), "data"
        )
        data_files: List[str] = [
            "bahamas_states_cities.json",
            "countries_states_cities.json",
        ]
        for data_file in data_files:
            print(f"Writing {data_file}...")
            for country in get_countries(
                file_path=os.path.join(data_directory, data_file)
            ):
                await country_repo.add(country=load_country(country=country))

        print("Countries seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_countries())
