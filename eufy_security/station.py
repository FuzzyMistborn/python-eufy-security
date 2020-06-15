"""Define a Eufy station object."""
import asyncio
from contextlib import asynccontextmanager
import logging
from typing import TYPE_CHECKING, Optional

from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import DeviceType, GuardMode, ParamType

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Station:
    """Define a station object (e.g. Homebase)."""

    def __init__(self, api: "API", station_info: dict) -> None:
        """Initialize."""
        self._api = api
        self.station_info: dict = station_info

    @asynccontextmanager
    async def async_establish_session(self, session: P2PSession = None):
        if session and session.valid_for(self.serial):
            yield session
            return

        async with self.connect() as session:
            yield session
            return

    @asynccontextmanager
    async def connect(self):
        dsk_key_resp = await self._api.request(
            "post", "app/equipment/get_dsk_keys", json={"station_sns": [self.serial]}
        )
        for item in dsk_key_resp.get("data")["dsk_keys"]:
            if item["station_sn"] == self.serial:
                p2p_session = P2PSession(
                    self.serial,
                    self.station_info["p2p_did"],
                    item["dsk_key"],
                    self.station_info["member"]["action_user_id"],
                )
                is_connected = await p2p_session.connect()
                if is_connected:
                    try:
                        yield p2p_session
                    finally:
                        await p2p_session.close()
                    return
                else:
                    raise EufySecurityP2PError(f"Could not connect to {self.name}")
        else:
            raise EufySecurityP2PError(f"Could not find discovery key for {self.name}")

    @property
    def device_type(self) -> str:
        """Return the station's device type."""
        return DeviceType(self.station_info["device_type"])

    @property
    def hardware_version(self) -> str:
        """Return the station's hardware version."""
        return self.station_info["main_hw_version"]

    @property
    def mac(self) -> str:
        """Return the station MAC address."""
        return self.station_info["wifi_mac"]

    @property
    def model(self) -> str:
        """Return the station's model."""
        return self.station_info["station_model"]

    @property
    def name(self) -> str:
        """Return the station name."""
        return self.station_info["station_name"]

    @property
    def params(self) -> dict:
        """Return station parameters."""
        params = {}
        for param in self.station_info["params"]:
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
        """Return the station serial number."""
        return self.station_info["station_sn"]

    @property
    def software_version(self) -> str:
        """Return the station's software version."""
        return self.station_info["main_sw_version"]

    @property
    def ip(self) -> str:
        """Return the station's ip."""
        return self.station_info["ip_addr"]

    async def async_update(self) -> None:
        """Get the latest values for the station's properties."""
        await self._api.async_update_device_info()

    async def set_guard_mode(self, mode: GuardMode, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int(
                0, CommandType.CMD_SET_ARMING, mode.value
            )
