"""Define a Eufy camera object."""
import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import DeviceType, ParamType

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Camera:
    """Define the camera object."""

    def __init__(self, api: "API", camera_info: dict) -> None:
        """Initialize."""
        self._api = api
        self.camera_info: dict = camera_info

    @staticmethod
    def from_info(api: "API", camera_info: dict) -> "Camera":
        camera_type = DeviceType(camera_info["device_type"])
        if camera_type == DeviceType.FLOODLIGHT:
            klass = FloodlightCamera
        elif camera_type == DeviceType.DOORBELL:
            klass = DoorbellCamera
        else:
            klass = Camera
        return klass(api, camera_info)

    @property
    def device_type(self) -> str:
        """Return the station's device type."""
        return DeviceType(self.camera_info["device_type"])

    @property
    def hardware_version(self) -> str:
        """Return the camera's hardware version."""
        return self.camera_info["main_hw_version"]

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest camera thumbnail."""
        return self.camera_info["cover_path"]

    @property
    def mac(self) -> str:
        """Return the camera MAC address."""
        return self.camera_info["wifi_mac"]

    @property
    def model(self) -> str:
        """Return the camera's model."""
        return self.camera_info["device_model"]

    @property
    def name(self) -> str:
        """Return the camera name."""
        return self.camera_info["device_name"]

    @property
    def params(self) -> dict:
        """Return camera parameters."""
        params = {}
        for param in self.camera_info["params"]:
            param_type = param["param_type"]
            value = param["param_value"]
            try:
                param_type = ParamType(param_type)
                value = param_type.read_value(value)
            except ValueError:
                _LOGGER.debug(
                    'Unable to process parameter "%s", value "%s"', param_type, value
                )
            params[param_type] = value
        return params

    @property
    def serial(self) -> str:
        """Return the camera serial number."""
        return self.camera_info["device_sn"]

    @property
    def software_version(self) -> str:
        """Return the camera's software version."""
        return self.camera_info["main_sw_version"]

    @property
    def station_serial(self) -> str:
        """Return the camera's station serial number."""
        return self.camera_info["station_sn"]

    async def async_set_params(self, params: dict) -> None:
        """Set camera parameters."""
        serialized_params = []
        for param_type, value in params.items():
            if isinstance(param_type, ParamType):
                value = param_type.write_value(value)
                param_type = param_type.value
            serialized_params.append({"param_type": param_type, "param_value": value})
        await self._api.request(
            "post",
            "app/upload_devs_params",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "params": serialized_params,
            },
        )
        await self.async_update()

    async def async_start_detection(self):
        """Start camera detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 1})

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

    async def async_stop_detection(self):
        """Stop camera detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 0})

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

    @asynccontextmanager
    async def async_establish_session(self, session: P2PSession = None):
        if session and session.valid_for(self.station_serial):
            yield session
            return

        if self.station_serial in self._api.stations:
            async with self._api.stations[self.station_serial].connect() as session:
                yield session
                return
        else:
            raise EufySecurityP2PError(f"Could not find station for {self.name}")


class DoorbellCamera(Camera):
    async def enable_osd(self, enable: bool, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_DEVS_OSD, 1 if enable else 0
            )


class FloodlightCamera(Camera):
    async def enable_osd(self, enable: bool, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            # 0 - disables the timestamp
            # 1 - enables timestamp but removes logo
            # 2 - enables all OSD items
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_DEVS_OSD, 2 if enable else 1
            )

    async def enable_manual_light(
        self, enable: bool, session: P2PSession = None
    ) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_FLOODLIGHT_MANUAL_SWITCH, 1 if enable else 0
            )
