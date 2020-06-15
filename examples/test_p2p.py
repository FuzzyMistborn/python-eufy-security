import asyncio
import logging
import os

from aiohttp import ClientSession

from eufy_security import async_login
from eufy_security.types import GuardMode

logging.basicConfig(level=logging.DEBUG)


EUFY_EMAIL = os.environ.get("EUFY_EMAIL")
EUFY_PASSWORD = os.environ.get("EUFY_PASSWORD")


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # Create an API client:
        api = await async_login(EUFY_EMAIL, EUFY_PASSWORD, websession)

        for station in api.stations.values():
            print("------------------")
            print(f"Station Name: {station.name}")
            print(f"Serial Number: {station.serial}")
            print(f"Station params: {station.params}")
            print(f"Station type: {station.device_type}")

            async with station.connect() as session:
                await station.set_guard_mode(GuardMode.AWAY, session)
                await asyncio.sleep(10)
                await station.set_guard_mode(GuardMode.HOME, session)
                await asyncio.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
