import asyncio
import logging
import os

from aiohttp import ClientSession

from eufy_security import async_login
from eufy_security.p2p.types import CommandType

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
            print(f"Camera params: {station.device_type}")

            async with station.connect() as session:
                print("Turning the on-screen watermark on")
                await session.async_set_command_with_int_string(
                    0, CommandType.CMD_SET_DEVS_OSD, 2
                )
                await asyncio.sleep(10)
                print("Turning watermark off")
                await session.async_set_command_with_int_string(
                    0, CommandType.CMD_SET_DEVS_OSD, 1
                )


asyncio.get_event_loop().run_until_complete(main())
