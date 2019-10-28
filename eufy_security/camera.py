"""Define a Eufy camera object."""
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api import API

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Camera:
    """Define the camera object."""

    def __init__(self, api: "API", camera_info: dict) -> None:
        """Initialize."""
        self._api = api
        self.camera_info: dict = camera_info

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest camera thumbnail."""
        return self.camera_info["cover_path"]

    @property
    def name(self) -> str:
        """Return the camera name."""
        return self.camera_info["device_name"]

    @property
    def serial(self) -> str:
        """Return the camera serial number."""
        return self.camera_info["device_sn"]

    @property
    def station_serial(self) -> str:
        """Return the camera's station serial number."""
        return self.camera_info["station_sn"]

    async def async_get_history(self) -> dict:
        """Get the camera's history."""
        history_resp = await self._api.request(
            "post", "event/app/get_all_history_record"
        )
        return history_resp["data"]

    async def async_start_stream(self) -> str:
        """Start the camera stream and return the RTSP URL."""
        start_resp = await self._api.request(
            "post",
            "web/equipment/start_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )

        return start_resp["data"]["url"]

    async def async_stop_stream(self) -> None:
        """Stop the camera stream."""
        await self._api.request(
            "post",
            "web/equipment/stop_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )

    async def async_update(self) -> None:
        """Get the latest values for the camera's properties."""
        await self._api.async_update_device_info()
