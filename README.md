# python-eufy-security

This is an experimental Python library for Eufy Security devices (cameras, doorbells, 
etc.).

# Python Versions

The library is currently supported on

* Python 3.6
* Python 3.7

# Installation

TBD

# Account Information

Because of the way the Eufy Security private API works, an email/password combo cannot
work with _both_ the Eufy Security mobile app _and_ this library. It is recommended to
use the mobile app to create a secondary "guest" account with a separate email address
and use it with this library.

# Usage

Everything starts with an:
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Login and get to work:

```python
import asyncio

from aiohttp import ClientSession

from eufy_security import async_login


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # Create an API client:
        api = await async_login(EUFY_EMAIL, EUFY_PASSWORD, websession)

        # Loop through the cameras associated with the account:
        for camera in api.cameras.values():
            print("------------------")
            print("Camera Name: %s", camera.name)
            print("Serial Number: %s", camera.serial)
            print("Station Serial Number: %s", camera.station_serial)
            print("Last Camera Image URL: %s", camera.last_camera_image_url)

            print("Starting RTSP Stream")
            stream_url = await camera.async_start_stream()
            print("Stream URL: %s", stream_url)

            print("Stopping RTSP Stream")
            stream_url = await camera.async_stop_stream()


asyncio.get_event_loop().run_until_complete(main())
```

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

# Contributing

1. [Check for open features/bugs](https://github.com/FuzzyMistborn/python-eufy-security/issues)
  or [initiate a discussion on one](https://github.com/FuzzyMistborn/python-eufy-security/issues/new).
2. [Fork the repository](https://github.com/FuzzyMistborn/python-eufy-security/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Submit a pull request!
