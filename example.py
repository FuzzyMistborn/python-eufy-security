"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from eufy_security import async_login
from eufy_security.errors import EufySecurityError

_LOGGER: logging.Logger = logging.getLogger()

EUFY_EMAIL: str = "<EMAIL>"
EUFY_PASSWORD: str = "<PASSWORD>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        try:
            # Create an API client:
            api = await async_login(EUFY_EMAIL, EUFY_PASSWORD, websession)

            # Loop through the cameras associated with the account:
            for camera in api.cameras.values():
                _LOGGER.info("------------------")
                _LOGGER.info("Camera Name: %s", camera.name)
                _LOGGER.info("Serial Number: %s", camera.serial)
                _LOGGER.info("Station Serial Number: %s", camera.station_serial)
                _LOGGER.info("Last Camera Image URL: %s", camera.last_camera_image_url)

                _LOGGER.info("Starting RTSP Stream")
                stream_url = await camera.async_start_stream()
                _LOGGER.info("Stream URL: %s", stream_url)

                _LOGGER.info("Stopping RTSP Stream")
                stream_url = await camera.async_stop_stream()
        except EufySecurityError as err:
            print(f"There was a/an {type(err)} error: {err}")


asyncio.get_event_loop().run_until_complete(main())
