from enum import Enum

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
