"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from eufy_security import async_login
from eufy_security.errors import EufySecurityError

EUFY_EMAIL = "<EMAIL>"
EUFY_PASSWORD = "<PASSWORD>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        try:
            # Create an API client:
            api = await async_login(EUFY_EMAIL, EUFY_PASSWORD, websession)

            # Loop through the cameras associated with the account:
            for camera in api.cameras.values():
                print(camera.name)
        except EufySecurityError as err:
            print(f"There was an error: {err}")


asyncio.get_event_loop().run_until_complete(main())
