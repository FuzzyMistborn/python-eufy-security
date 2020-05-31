"""Define parameters that can be sent to the base station."""
import base64
from enum import Enum
import json


class DeviceType(Enum):
    """
    List retrieved from com.oceanwing.battery.cam.binder.model.QueryDeviceData
    """

    BATTERY_DOORBELL = 7
    CAMERA = 1
    CAMERA2 = 9
    CAMERA2C = 8
    CAMERA_E = 4
    DOORBELL = 5
    FLOODLIGHT = 3
    INDOOR_CAMERA = 30
    INDOOR_PT_CAMERA = 31
    KEYPAD = 11
    LOCK_ADVANCED = 51
    LOCK_BASIC = 50
    LOCK_SIMPLE = 52
    MOTION_SENSOR = 10
    SENSOR = 2
    STATION = 0

    def is_doorbell(self):
        return self in [
            DeviceType.BATTERY_DOORBELL,
            DeviceType.DOORBELL,
        ]

    def is_camera(self):
        return self in [
            DeviceType.BATTERY_DOORBELL,
            DeviceType.DOORBELL,
            DeviceType.CAMERA,
            DeviceType.CAMERA2,
            DeviceType.CAMERA2C,
            DeviceType.CAMERA_E,
            DeviceType.FLOODLIGHT,
            DeviceType.INDOOR_CAMERA,
            DeviceType.INDOOR_PT_CAMERA,
        ]

    def is_station(self):
        return self in [DeviceType.DOORBELL, DeviceType.FLOODLIGHT, DeviceType.STATION]


class ParamType(Enum):
    """
    List retrieved from com.oceanwing.battery.cam.binder.model.CameraParams
    """

    CHIME_STATE = 2015
    DETECT_EXPOSURE = 2023
    DETECT_MODE = 2004
    DETECT_MOTION_SENSITIVE = 2005
    DETECT_SCENARIO = 2028
    DETECT_SWITCH = 2027
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

    # Inferred from source
    SNOOZE_MODE = 1271  # The value is base64 encoded
    WATERMARK_MODE = 1214  # 1 - hide, 2 - show
    DEVICE_UPGRADE_NOW = 1134
    CAMERA_UPGRADE_NOW = 1133
    SCHEDULE_MODE = 1257
    GUARD_MODE = 1224  # 0 - Away, 1 - Home, 63 - Disarmed, 2 - chedule

    FLOODLIGHT_MANUAL_SWITCH = 1400
    FLOODLIGHT_MANUAL_BRIGHTNESS = 1401  # The range is 22-100
    FLOODLIGHT_MOTION_BRIGHTNESS = 1412  # The range is 22-100
    FLOODLIGHT_SCHEDULE_BRIGHTNESS = 1413  # The range is 22-100
    FLOODLIGHT_MOTION_SENSITIVTY = 1272  # The range is 1-5

    CAMERA_SPEAKER_VOLUME = 1230
    CAMERA_RECORD_ENABLE_AUDIO = 1366  # Enable microphone
    CAMERA_RECORD_RETRIGGER_INTERVAL = 1250  # In seconds
    CAMERA_RECORD_CLIP_LENGTH = 1249  # In seconds

    CAMERA_IR_CUT = 1013
    CAMERA_PIR = 1011
    CAMERA_WIFI_RSSI = 1142

    CAMERA_MOTION_ZONES = 1204

    # Set only params?
    PUSH_MSG_MODE = 1252  # 0 to ???

    def read_value(self, value):
        """Read a parameter JSON string."""
        if value:
            if self in [ParamType.SNOOZE_MODE, ParamType.CAMERA_MOTION_ZONES]:
                value = base64.b64decode(value, validate=True).decode()
            return json.loads(value)
        return None

    def write_value(self, value):
        """Write a parameter JSON string."""
        value = json.dumps(value)
        if self is ParamType.SNOOZE_MODE:
            value = base64.b64encode(value.encode()).decode()
        return value
