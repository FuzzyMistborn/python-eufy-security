"""Define a base object for interacting with the Eufy camera API."""
from datetime import datetime
import logging
from typing import Dict, Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .camera import Camera
from .errors import InvalidCredentialsError, RequestError, raise_error

_LOGGER: logging.Logger = logging.getLogger(__name__)

API_BASE: str = "https://mysecurity.eufylife.com/api/v1"


class API:  # pylint: disable=too-many-instance-attributes
    """Define the API object."""

    def __init__(self, email: str, password: str, websession: ClientSession) -> None:
        """Initialize."""
        self._api_base: str = API_BASE
        self._email: str = email
        self._password: str = password
        self._retry_on_401: bool = False
        self._session: ClientSession = websession
        self._token: Optional[str] = None
        self._token_expiration: Optional[datetime] = None

        self.cameras: Dict[str, Camera] = {}

    async def async_authenticate(self) -> None:
        """Authenticate and get an access token."""
        auth_resp = await self.request(
            "post",
            "passport/login",
            json={"email": self._email, "password": self._password},
        )

        self._retry_on_401 = False
        self._token = auth_resp["data"]["auth_token"]
        self._token_expiration = datetime.fromtimestamp(
            auth_resp["data"]["token_expires_at"]
        )
        domain = auth_resp["data"].get("domain")
        if domain:
            self._api_base = f"https://{domain}/v1"
            _LOGGER.info("Switching to another API_BASE: %s", self._api_base)

    async def async_get_history(self) -> dict:
        """Get the camera's history."""
        history_resp = await self.request("post", "event/app/get_all_history_record")
        return history_resp["data"]

    async def async_update_device_info(self) -> None:
        """Get the latest device info."""
        devices_resp = await self.request("post", "app/get_devs_list")

        if not devices_resp.get("data"):
            return

        for device_info in devices_resp["data"]:
            if device_info["device_sn"] in self.cameras:
                camera = self.cameras[device_info["device_sn"]]
                camera.camera_info = device_info
                continue
            self.cameras[device_info["device_sn"]] = Camera(self, device_info)

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """Make a request the API.com."""
        if self._token_expiration and datetime.now() >= self._token_expiration:
            _LOGGER.info("Access token expired; fetching a new one")
            self._token = None
            self._token_expiration = None
            await self.async_authenticate()

        url: str = f"{self._api_base}/{endpoint}"

        if not headers:
            headers = {}
        if self._token:
            headers["x-auth-token"] = self._token

        async with self._session.request(
            method, url, headers=headers, json=json
        ) as resp:
            try:
                resp.raise_for_status()
                data: dict = await resp.json(content_type=None)

                if not data:
                    raise RequestError(f"No response while requesting {endpoint}")

                _raise_on_error(data)

                return data
            except ClientError as err:
                if "401" in str(err):
                    if self._retry_on_401:
                        raise InvalidCredentialsError("Token failed multiple times")

                    self._retry_on_401 = True
                    await self.async_authenticate()
                    return await self.request(
                        method, endpoint, headers=headers, json=json
                    )
                raise RequestError(
                    f"There was an unknown error while requesting {endpoint}: {err}"
                ) from None


def _raise_on_error(data: dict) -> None:
    """Raise appropriately when a returned data payload contains an error."""
    if data["code"] == 0:
        return
    raise_error(data)


async def async_login(email: str, password: str, websession: ClientSession) -> API:
    """Return an authenticated API object."""
    api: API = API(email, password, websession)
    await api.async_authenticate()
    await api.async_update_device_info()
    return api
