from enum import Enum


class P2PClientProtocolRequestMessageType(Enum):
    STUN = bytes([0xF1, 0x00])
    LOOKUP = bytes([0xF1, 0x20])
    LOOKUP_WITH_KEY = bytes([0xF1, 0x26])
    LOCAL_LOOKUP = bytes([0xF1, 0x30])
    PING = bytes([0xF1, 0xE0])
    PONG = bytes([0xF1, 0xE1])
    CHECK_CAM = bytes([0xF1, 0x41])
    DATA = bytes([0xF1, 0xD0])
    ACK = bytes([0xF1, 0xD1])
    END = bytes([0xF1, 0xF0])


class P2PClientProtocolResponseMessageType(Enum):
    STUN = bytes([0xF1, 0x01])
    LOOKUP_RESP = bytes([0xF1, 0x21])
    LOOKUP_ADDR = bytes([0xF1, 0x40])
    LOCAL_LOOKUP_RESP = bytes([0xF1, 0x41])
    END = bytes([0xF1, 0xF0])
    PONG = bytes([0xF1, 0xE1])
    PING = bytes([0xF1, 0xE0])
    CAM_ID = bytes([0xF1, 0x42])
    ACK = bytes([0xF1, 0xD1])
    DATA = bytes([0xF1, 0xD0])


class EufyP2PDataType(Enum):
    DATA = bytes([0xD1, 0x00])
    VIDEO = bytes([0xD1, 0x01])
    CONTROL = bytes([0xD1, 0x02])


class CommandType(Enum):
    ARM_DELAY_AWAY = 1158
    ARM_DELAY_CUS1 = 1159
    ARM_DELAY_CUS2 = 1160
    ARM_DELAY_CUS3 = 1161
    ARM_DELAY_HOME = 1157
    AUTOMATION_DATA = 1278
    AUTOMATION_ID_LIST = 1165
    CMD_ALARM_DELAY_AWAY = 1167
    CMD_ALARM_DELAY_CUSTOM1 = 1168
    CMD_ALARM_DELAY_CUSTOM2 = 1169
    CMD_ALARM_DELAY_CUSTOM3 = 1170
    CMD_ALARM_DELAY_HOME = 1166
    CMD_AUDDEC_SWITCH = 1017
    CMD_AUDIO_FRAME = 1301
    CMD_BATCH_RECORD = 1049
    CMD_BAT_DOORBELL_CHIME_SWITCH = 1702
    CMD_BAT_DOORBELL_MECHANICAL_CHIME_SWITCH = 1703
    CMD_BAT_DOORBELL_QUICK_RESPONSE = 1706
    CMD_BAT_DOORBELL_SET_ELECTRONIC_RINGTONE_TIME = 1709
    CMD_BAT_DOORBELL_SET_LED_ENABLE = 1716
    CMD_BAT_DOORBELL_SET_NOTIFICATION_MODE = 1710
    CMD_BAT_DOORBELL_SET_RINGTONE_VOLUME = 1708
    CMD_BAT_DOORBELL_UPDATE_QUICK_RESPONSE = 1707
    CMD_BAT_DOORBELL_VIDEO_QUALITY = 1705
    CMD_BAT_DOORBELL_WDR_SWITCH = 1704
    CMD_BIND_BROADCAST = 1000
    CMD_BIND_SYNC_ACCOUNT_INFO = 1001
    CMD_BIND_SYNC_ACCOUNT_INFO_EX = 1054
    CMD_CAMERA_INFO = 1103
    CMD_CHANGE_PWD = 1030
    CMD_CHANGE_WIFI_PWD = 1031
    CMD_CLOSE_AUDDEC = 1018
    CMD_CLOSE_DEV_LED = 1046
    CMD_CLOSE_EAS = 1016
    CMD_CLOSE_IRCUT = 1014
    CMD_CLOSE_PIR = 1012
    CMD_COLLECT_RECORD = 1047
    CMD_CONVERT_MP4_OK = 1303
    CMD_DECOLLECT_RECORD = 1048
    CMD_DELLETE_RECORD = 1027
    CMD_DEL_FACE_PHOTO = 1234
    CMD_DEL_USER_PHOTO = 1232
    CMD_DEVS_BIND_BROADCASE = 1038
    CMD_DEVS_BIND_NOTIFY = 1039
    CMD_DEVS_LOCK = 1019
    CMD_DEVS_SWITCH = 1035
    CMD_DEVS_TO_FACTORY = 1037
    CMD_DEVS_UNBIND = 1040
    CMD_DEVS_UNLOCK = 1020
    CMD_DEV_LED_SWITCH = 1045
    CMD_DEV_PUSHMSG_MODE = 1252
    CMD_DEV_RECORD_AUTOSTOP = 1251
    CMD_DEV_RECORD_INTERVAL = 1250
    CMD_DEV_RECORD_TIMEOUT = 1249
    CMD_DOENLOAD_FINISH = 1304
    CMD_DOORBELL_NOTIFY_PAYLOAD = 1701
    CMD_DOORBELL_SET_PAYLOAD = 1700
    CMD_DOOR_SENSOR_ALARM_ENABLE = 1506
    CMD_DOOR_SENSOR_DOOR_EVT = 1503
    CMD_DOOR_SENSOR_ENABLE_LED = 1505
    CMD_DOOR_SENSOR_GET_DOOR_STATE = 1502
    CMD_DOOR_SENSOR_GET_INFO = 1501
    CMD_DOOR_SENSOR_INFO_REPORT = 1500
    CMD_DOOR_SENSOR_LOW_POWER_REPORT = 1504
    CMD_DOWNLOAD_CANCEL = 1051
    CMD_DOWNLOAD_VIDEO = 1024
    CMD_EAS_SWITCH = 1015
    CMD_ENTRY_SENSOR_BAT_STATE = 1552
    CMD_ENTRY_SENSOR_CHANGE_TIME = 1551
    CMD_ENTRY_SENSOR_STATUS = 1550
    CMD_FLOODLIGHT_BROADCAST = 902
    CMD_FORMAT_SD = 1029
    CMD_FORMAT_SD_PROGRESS = 1053
    CMD_GATEWAYINFO = 1100
    CMD_GEO_ADD_USER_INFO = 1259
    CMD_GEO_DEL_USER_INFO = 1261
    CMD_GEO_SET_USER_STATUS = 1258
    CMD_GEO_UPDATE_LOC_SETTING = 1262
    CMD_GEO_UPDATE_USER_INFO = 1260
    CMD_GET_ADMIN_PWD = 1122
    CMD_GET_ALARM_MODE = 1151
    CMD_GET_ARMING_INFO = 1107
    CMD_GET_ARMING_STATUS = 1108
    CMD_GET_AUDDEC_INFO = 1109
    CMD_GET_AUDDEC_SENSITIVITY = 1110
    CMD_GET_AUDDE_CSTATUS = 1111
    CMD_GET_AWAY_ACTION = 1239
    CMD_GET_BATTERY = 1101
    CMD_GET_BATTERY_TEMP = 1138
    CMD_GET_CAMERA_LOCK = 1119
    CMD_GET_CHARGE_STATUS = 1136
    CMD_GET_CUSTOM1_ACTION = 1148
    CMD_GET_CUSTOM2_ACTION = 1149
    CMD_GET_CUSTOM3_ACTION = 1150
    CMD_GET_DELAY_ALARM = 1164
    CMD_GET_DEVICE_PING = 1152
    CMD_GET_DEVS_NAME = 1129
    CMD_GET_DEVS_RSSI_LIST = 1274
    CMD_GET_DEV_STATUS = 1131
    CMD_GET_DEV_TONE_INFO = 1127
    CMD_GET_DEV_UPGRADE = 1134
    CMD_GET_EAS_STATUS = 1118
    CMD_GET_EXCEPTION_LOG = 1124
    CMD_GET_FLOODLIGHT_WIFI_LIST = 1405
    CMD_GET_GATEWAY_LOCK = 1120
    CMD_GET_HOME_ACTION = 1225
    CMD_GET_HUB_LAN_IP = 1176
    CMD_GET_HUB_LOG = 1132
    CMD_GET_HUB_LOGIG = 1140
    CMD_GET_HUB_NAME = 1128
    CMD_GET_HUB_POWWER_SUPPLY = 1137
    CMD_GET_HUB_TONE_INFO = 1126
    CMD_GET_HUB_UPGRADE = 1133
    CMD_GET_IRCUTSENSITIVITY = 1114
    CMD_GET_IRMODE = 1113
    CMD_GET_MDETECT_PARAM = 1105
    CMD_GET_MIRRORMODE = 1112
    CMD_GET_NEWVESION = 1125
    CMD_GET_OFF_ACTION = 1177
    CMD_GET_P2P_CONN_STATUS = 1130
    CMD_GET_PIRCTRL = 1116
    CMD_GET_PIRINFO = 1115
    CMD_GET_PIRSENSITIVITY = 1117
    CMD_GET_RECORD_TIME = 1104
    CMD_GET_REPEATER_CONN_TEST_RESULT = 1270
    CMD_GET_REPEATER_RSSI = 1266
    CMD_GET_REPEATER_SITE_LIST = 1263
    CMD_GET_START_HOMEKIT = 1163
    CMD_GET_SUB1G_RSSI = 1141
    CMD_GET_TFCARD_FORMAT_STATUS = 1143
    CMD_GET_TFCARD_REPAIR_STATUS = 1153
    CMD_GET_TFCARD_STATUS = 1135
    CMD_GET_UPDATE_STATUS = 1121
    CMD_GET_UPGRADE_RESULT = 1043
    CMD_GET_WAN_LINK_STATUS = 1268
    CMD_GET_WAN_MODE = 1265
    CMD_GET_WIFI_PWD = 1123
    CMD_GET_WIFI_RSSI = 1142
    CMD_HUB_ALARM_TONE = 1281
    CMD_HUB_CLEAR_EMMC_VOLUME = 1800
    CMD_HUB_NOTIFY_ALARM = 1282
    CMD_HUB_NOTIFY_MODE = 1283
    CMD_HUB_REBOOT = 1034
    CMD_HUB_TO_FACTORY = 1036
    CMD_IRCUT_SWITCH = 1013
    CMD_KEYPAD_BATTERY_CAP_STATE = 1653
    CMD_KEYPAD_BATTERY_CHARGER_STATE = 1655
    CMD_KEYPAD_BATTERY_TEMP_STATE = 1654
    CMD_KEYPAD_GET_PASSWORD = 1657
    CMD_KEYPAD_GET_PASSWORD_LIST = 1662
    CMD_KEYPAD_IS_PSW_SET = 1670
    CMD_KEYPAD_PSW_OPEN = 1664
    CMD_KEYPAD_SET_CUSTOM_MAP = 1660
    CMD_KEYPAD_SET_PASSWORD = 1650
    CMD_LEAVING_DELAY_AWAY = 1172
    CMD_LEAVING_DELAY_CUSTOM1 = 1173
    CMD_LEAVING_DELAY_CUSTOM2 = 1174
    CMD_LEAVING_DELAY_CUSTOM3 = 1175
    CMD_LEAVING_DELAY_HOME = 1171
    CMD_LIVEVIEW_LED_SWITCH = 1056
    CMD_MDETECTINFO = 1106
    CMD_MOTION_SENSOR_BAT_STATE = 1601
    CMD_MOTION_SENSOR_ENABLE_LED = 1607
    CMD_MOTION_SENSOR_ENTER_USER_TEST_MODE = 1613
    CMD_MOTION_SENSOR_EXIT_USER_TEST_MODE = 1610
    CMD_MOTION_SENSOR_PIR_EVT = 1605
    CMD_MOTION_SENSOR_SET_CHIRP_TONE = 1611
    CMD_MOTION_SENSOR_SET_PIR_SENSITIVITY = 1609
    CMD_MOTION_SENSOR_WORK_MODE = 1612
    CMD_NAS_SWITCH = 1145
    CMD_NAS_TEST = 1146
    CMD_NOTIFY_PAYLOAD = 1351
    CMD_P2P_DISCONNECT = 1044
    CMD_PING = 1139
    CMD_PIR_SWITCH = 1011
    CMD_RECORDDATE_SEARCH = 1041
    CMD_RECORDLIST_SEARCH = 1042
    CMD_RECORD_AUDIO_SWITCH = 1366
    CMD_RECORD_IMG = 1021
    CMD_RECORD_IMG_STOP = 1022
    CMD_RECORD_PLAY_CTRL = 1026
    CMD_RECORD_VIEW = 1025
    CMD_REPAIR_PROGRESS = 1058
    CMD_REPAIR_SD = 1057
    CMD_REPEATER_RSSI_TEST = 1269
    CMD_SDINFO = 1102
    CMD_SDINFO_EX = 1144
    CMD_SENSOR_SET_CHIRP_TONE = 1507
    CMD_SENSOR_SET_CHIRP_VOLUME = 1508
    CMD_SET_AI_NICKNAME = 1242
    CMD_SET_AI_PHOTO = 1231
    CMD_SET_AI_SWITCH = 1236
    CMD_SET_ALL_ACTION = 1255
    CMD_SET_ARMING = 1224
    CMD_SET_ARMING_SCHEDULE = 1211
    CMD_SET_AS_SERVER = 1237
    CMD_SET_AUDDEC_INFO = 1212
    CMD_SET_AUDDEC_SENSITIVITY = 1213
    CMD_SET_AUDIOSENSITIVITY = 1227
    CMD_SET_AUTO_DELETE_RECORD = 1367
    CMD_SET_BITRATE = 1206
    CMD_SET_CUSTOM_MODE = 1256
    CMD_SET_DEVS_NAME = 1217
    CMD_SET_DEVS_OSD = 1214
    CMD_SET_DEVS_TONE_FILE = 1202
    CMD_SET_DEV_MD_RECORD = 1273
    CMD_SET_DEV_MIC_MUTE = 1240
    CMD_SET_DEV_MIC_VOLUME = 1229
    CMD_SET_DEV_SPEAKER_MUTE = 1241
    CMD_SET_DEV_SPEAKER_VOLUME = 1230
    CMD_SET_DEV_STORAGE_TYPE = 1228
    CMD_SET_FLOODLIGHT_BRIGHT_VALUE = 1401
    CMD_SET_FLOODLIGHT_DETECTION_AREA = 1407
    CMD_SET_FLOODLIGHT_LIGHT_SCHEDULE = 1404
    CMD_SET_FLOODLIGHT_MANUAL_SWITCH = 1400
    CMD_SET_FLOODLIGHT_STREET_LAMP = 1402
    CMD_SET_FLOODLIGHT_TOTAL_SWITCH = 1403
    CMD_SET_FLOODLIGHT_WIFI_CONNECT = 1406
    CMD_SET_GSSENSITIVITY = 1226
    CMD_SET_HUB_ALARM_AUTO_END = 1280
    CMD_SET_HUB_ALARM_CLOSE = 1279
    CMD_SET_HUB_AUDEC_STATUS = 1222
    CMD_SET_HUB_GS_STATUS = 1220
    CMD_SET_HUB_IRCUT_STATUS = 1219
    CMD_SET_HUB_MVDEC_STATUS = 1221
    CMD_SET_HUB_NAME = 1216
    CMD_SET_HUB_OSD = 1253
    CMD_SET_HUB_PIR_STATUS = 1218
    CMD_SET_HUB_SPK_VOLUME = 1235
    CMD_SET_IRMODE = 1208
    CMD_SET_JSON_SCHEDULE = 1254
    CMD_SET_LANGUAGE = 1200
    CMD_SET_LIGHT_CTRL_BRIGHT_PIR = 1412
    CMD_SET_LIGHT_CTRL_BRIGHT_SCH = 1413
    CMD_SET_LIGHT_CTRL_LAMP_VALUE = 1410
    CMD_SET_LIGHT_CTRL_PIR_SWITCH = 1408
    CMD_SET_LIGHT_CTRL_PIR_TIME = 1409
    CMD_SET_LIGHT_CTRL_SUNRISE_INFO = 1415
    CMD_SET_LIGHT_CTRL_SUNRISE_SWITCH = 1414
    CMD_SET_LIGHT_CTRL_TRIGGER = 1411
    CMD_SET_MDETECTPARAM = 1204
    CMD_SET_MDSENSITIVITY = 1272
    CMD_SET_MIRRORMODE = 1207
    CMD_SET_MOTION_SENSITIVITY = 1276
    CMD_SET_NIGHT_VISION_TYPE = 1277
    CMD_SET_NOTFACE_PUSHMSG = 1248
    CMD_SET_PAYLOAD = 1350
    CMD_SET_PIRSENSITIVITY = 1210
    CMD_SET_PIR_INFO = 1209
    CMD_SET_PIR_POWERMODE = 1246
    CMD_SET_PIR_TEST_MODE = 1243
    CMD_SET_PRI_ACTION = 1233
    CMD_SET_RECORDTIME = 1203
    CMD_SET_REPEATER_PARAMS = 1264
    CMD_SET_RESOLUTION = 1205
    CMD_SET_SCHEDULE_DEFAULT = 1257
    CMD_SET_SNOOZE_MODE = 1271
    CMD_SET_STORGE_TYPE = 1223
    CMD_SET_TELNET = 1247
    CMD_SET_TIMEZONE = 1215
    CMD_SET_TONE_FILE = 1201
    CMD_SET_UPGRADE = 1238
    CMD_SNAPSHOT = 1028
    CMD_START_REALTIME_MEDIA = 1003
    CMD_START_RECORD = 1009
    CMD_START_REC_BROADCASE = 900
    CMD_START_TALKBACK = 1005
    CMD_START_VOICECALL = 1007
    CMD_STOP_REALTIME_MEDIA = 1004
    CMD_STOP_RECORD = 1010
    CMD_STOP_REC_BROADCASE = 901
    CMD_STOP_SHARE = 1023
    CMD_STOP_TALKBACK = 1006
    CMD_STOP_VOICECALL = 1008
    CMD_STREAM_MSG = 1302
    CMD_STRESS_TEST_OPER = 1050
    CMD_TIME_SYCN = 1033
    CMD_UNBIND_ACCOUNT = 1002
    CMD_VIDEO_FRAME = 1300
    CMD_WIFI_CONFIG = 1032
