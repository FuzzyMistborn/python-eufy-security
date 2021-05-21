"""Define a Eufy device object."""
import logging
from typing import TYPE_CHECKING

from .types import DeviceType
from .params import ParamType

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Device:
    """Define the device object."""

    def __init__(self, api: "API", device_info: dict) -> None:
        """Initialize."""
        self._api = api
        self.device_info = device_info

    def update(self, device_info: dict) -> None:
        """Update the device's info."""
        self.device_info = device_info

    @property
    def type(self) -> DeviceType:
        """Return the device's type."""
        return DeviceType(self.device_info["device_type"])

    @property
    def is_camera(self) -> bool:
        """Return whether device is a camera."""
        return self.type.is_camera

    @property
    def is_station(self) -> bool:
        """Return whether device is a station."""
        return self.type.is_station

    @property
    def is_sensor(self) -> bool:
        """Return whether device is a sensor."""
        return self.type.is_sensor

    @property
    def is_doorbell(self) -> bool:
        """Return whether device is a doorbell."""
        return self.type.is_doorbell

    @property
    def serial(self) -> str:
        """Return the device's serial number."""
        return self.device_info["device_sn"]

    @property
    def station_serial(self) -> str:
        """Return the device's station serial number."""
        return self.device_info["station_sn"]

    @property
    def software_version(self) -> str:
        """Return the device's software version."""
        return self.device_info["main_sw_version"]

    @property
    def hardware_version(self) -> str:
        """Return the device's hardware version."""
        return self.device_info["main_hw_version"]

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest device thumbnail."""
        return self.device_info["cover_path"]

    @property
    def mac(self) -> str:
        """Return the device MAC address."""
        return self.device_info["wifi_mac"]

    @property
    def model(self) -> str:
        """Return the device's model."""
        return self.device_info["device_model"]

    @property
    def name(self) -> str:
        """Return the device name."""
        return self.device_info["device_name"]

    @property
    def params(self) -> dict:
        """Return device parameters."""
        params = {}
        for param in self.device_info["params"]:
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

    async def async_set_params(self, params: dict) -> None:
        """Set device parameters."""
        await self._api.async_set_params(self, params)

    async def async_start_detection(self):
        """Start device detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 1})

    async def async_start_stream(self) -> str:
        """Start the device stream and return the RTSP URL."""
        return await self._api.async_start_stream(self)

    async def async_stop_detection(self):
        """Stop device detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 0})

    async def async_stop_stream(self) -> None:
        """Stop the device stream."""
        await self._api.async_stop_stream(self)

    async def async_update(self) -> None:
        """Get the latest values for the device's properties."""
        await self._api.async_update_device_info()
