"""Define types."""
from enum import Enum

from .converters import (
    BoolConverter,
    JsonBase64Converter,
    JsonConverter,
    NumberConverter,
    StringConverter,
)


class DeviceType(Enum):
    """List of device types."""

    # List retrieved from com.oceanwing.battery.cam.binder.model.QueryDeviceData

    BATTERY_DOORBELL = 7
    BATTERY_DOORBELL_2 = 16
    CAMERA = 1
    CAMERA2 = 9
    CAMERA2C = 8
    CAMERA2C_PRO = 15
    CAMERA2_PRO = 14
    CAMERA_E = 4
    DOORBELL = 5
    FLOODLIGHT = 3
    INDOOR_CAMERA = 30
    INDOOR_CAMERA_1080 = 34
    INDOOR_PT_CAMERA = 31
    INDOOR_PT_CAMERA_1080 = 35
    KEYPAD = 11
    LOCK_ADVANCED = 51
    LOCK_ADVANCED_NO_FINGER = 53
    LOCK_BASIC = 50
    LOCK_BASIC_NO_FINGER = 52
    MOTION_SENSOR = 10
    SENSOR = 2
    SOLO_CAMERA = 32
    SOLO_CAMERA_PRO = 33
    STATION = 0

    @property
    def is_camera(self) -> bool:
        """Return whether device type is a camera."""
        return self in [
            DeviceType.CAMERA,
            DeviceType.CAMERA2,
            DeviceType.CAMERA_E,
            DeviceType.CAMERA2C,
            DeviceType.INDOOR_CAMERA,
            DeviceType.INDOOR_PT_CAMERA,
            DeviceType.FLOODLIGHT,
            DeviceType.DOORBELL,
            DeviceType.BATTERY_DOORBELL,
            DeviceType.BATTERY_DOORBELL_2,
            DeviceType.CAMERA2C_PRO,
            DeviceType.CAMERA2_PRO,
            DeviceType.INDOOR_CAMERA_1080,
            DeviceType.INDOOR_PT_CAMERA_1080,
            DeviceType.SOLO_CAMERA,
            DeviceType.SOLO_CAMERA_PRO,
        ]

    @property
    def is_station(self) -> bool:
        """Return whether device type is a station."""
        return self in [
            DeviceType.STATION,
        ]

    @property
    def is_sensor(self) -> bool:
        """Return whether device type is a sensor."""
        return self in [
            DeviceType.SENSOR,
            DeviceType.MOTION_SENSOR,
        ]

    @property
    def is_doorbell(self) -> bool:
        """Return whether device type is a doorbell."""
        return self in [
            DeviceType.DOORBELL,
            DeviceType.BATTERY_DOORBELL,
            DeviceType.BATTERY_DOORBELL_2,
        ]


class ParamType(Enum):
    """Define the types.

    List retrieved from from com.oceanwing.battery.cam.binder.model.CameraParams
    """

    def __new__(cls, value, converter=NumberConverter):
        """Create a new ParamType."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj._converter_ = converter
        return obj

    def loads(self, value):
        """Read a parameter JSON string."""
        return self._converter_.loads(value)

    def dumps(self, value):
        """Write a parameter JSON string."""
        return self._converter_.dumps(value)

    CHIME_STATE = 2015
    DETECT_EXPOSURE = 2023
    DETECT_MODE = 2004
    DETECT_MOTION_SENSITIVE = 2005
    DETECT_SCENARIO = 2028
    DETECT_SWITCH = 2027, JsonConverter
    DETECT_ZONE = 2006
    DOORBELL_AUDIO_RECODE = 2042
    DOORBELL_BRIGHTNESS = 2032
    DOORBELL_DISTORTION = 2033
    DOORBELL_HDR = 2029
    DOORBELL_IR_MODE = 2030
    DOORBELL_LED_NIGHT_MODE = 2039
    DOORBELL_MOTION_ADVANCE_OPTION = 2041
    DOORBELL_MOTION_NOTIFICATION = 2035
    DOORBELL_NOTIFICATION_JUMP_MODE = 2038
    DOORBELL_NOTIFICATION_OPEN = 2036
    DOORBELL_RECORD_QUALITY = 2034
    DOORBELL_RING_RECORD = 2040
    DOORBELL_SNOOZE_START_TIME = 2037
    DOORBELL_VIDEO_QUALITY = 2031
    NIGHT_VISUAL = 2002
    OPEN_DEVICE = 2001
    RINGING_VOLUME = 2022
    SDCARD = 2010
    UN_DETECT_ZONE = 2007
    VOLUME = 2003

    COMMAND_LED_NIGHT_OPEN = 1026
    COMMAND_MOTION_DETECTION_PACKAGE = 1016

    # Inferred from source
    SNOOZE_MODE = 1271, JsonBase64Converter
    WATERMARK_MODE = 1214  # 1 - hide, 2 - show
    DEVICE_UPGRADE_NOW = 1134
    CAMERA_UPGRADE_NOW = 1133
    DEFAULT_SCHEDULE_MODE = 1257  # 0 - Away, 1 - Home, 63 - Disarmed
    GUARD_MODE = 1224  # 0 - Away, 1 - Home, 63 - Disarmed, 2 - Schedule

    FLOODLIGHT_MANUAL_SWITCH = 1400
    FLOODLIGHT_MANUAL_BRIGHTNESS = 1401  # The range is 22-100
    FLOODLIGHT_MOTION_BRIGHTNESS = 1412  # The range is 22-100
    FLOODLIGHT_SCHEDULE_BRIGHTNESS = 1413  # The range is 22-100
    FLOODLIGHT_MOTION_SENSITIVTY = 1272  # The range is 1-5

    CAMERA_SPEAKER_VOLUME = 1230
    CAMERA_RECORD_ENABLE_AUDIO = 1366, BoolConverter
    CAMERA_RECORD_RETRIGGER_INTERVAL = 1250  # In seconds
    CAMERA_RECORD_CLIP_LENGTH = 1249  # In seconds

    CAMERA_IR_CUT = 1013
    CAMERA_PIR = 1011, BoolConverter
    CAMERA_WIFI_RSSI = 1142

    CAMERA_MOTION_ZONES = 1204, JsonBase64Converter

    # Set only params?
    PUSH_MSG_MODE = 1252  # 0 to ???

    PRIVATE_MODE = 99904, BoolConverter
    CUSTOM_RTSP_URL = 999991, StringConverter
