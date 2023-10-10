import sys

sys.path.append("/usr/src/app")

from db.seeder.seed_countries import seed_countries
import asyncio

if __name__ == "__main__":
    asyncio.run(seed_countries())
