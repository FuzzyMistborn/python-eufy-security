"""Define parameters that can be sent to the base station."""
import base64
from enum import Enum
import json


class ParamType(Enum):
    """Define the types.

    List retrieved from from com.oceanwing.battery.cam.binder.model.CameraParams
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

    # Set only params?
    PUSH_MSG_MODE = 1252  # 0 to ???

    def read_value(self, value):
        """Read a parameter JSON string."""
        if value:
            if self is ParamType.SNOOZE_MODE:
                value = base64.b64decode(value, validate=True).decode()
            return json.loads(value)
        return None

    def write_value(self, value):
        """Write a parameter JSON string."""
        value = json.dumps(value)
        if self is ParamType.SNOOZE_MODE:
            value = base64.b64encode(value.encode()).decode()
        return value
