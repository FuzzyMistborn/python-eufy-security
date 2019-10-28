# python-eufy-security
Python library for Eufy Security cameras

# API Calls/Documentation

## Login

POST `https://mysecurity.eufylife.com/api/v1/passport/login`

Body:
```
{
  "email": "youremail@domain.tld",
  "password": "your password"
}
```

Response
```
{
    "code": 0,
    "msg": "Succeed.",
    "data": {
        "user_id": "REDACTED",
        "email": "youremail@domain.tld",
        "nick_name": "youremail",
        "auth_token": "AUTH_TOKEN_HERE",
        "token_expires_at": 1565717940,
        "avatar": "",
        "invitation_code": "REDACTED",
        "inviter_code": "",
        "mac_addr": "REDACTED",
        "domain": "security-app.eufylife.com",
        "ab_code": "US",
        "geo_key": "REDACTED",
        "privilege": 0,
        "params": null
    }
}
```
The important part of that one is the auth_token which is used in any further requests.

## List Devices
POST `https://mysecurity.eufylife.com/api/v1/app/get_devs_list`

Headers:

`x-auth-token: AUTH_TOKEN_HERE`

Body:
```
{
	"device_sn": "",
	"num": 100,
	"orderby": "",
	"page": 0,
	"station_sn": ""
}
```

Response
```
{
    "code": 0,
    "msg": "Succeed.",
    "data": [
        {
            "device_id": REDACTED,
            "device_sn": "REDACTED",
            "device_name": "Doorbell",
            "device_model": "T8200",
            "time_zone": "EST5EDT,M3.2.0,M11.1.0",
            "device_type": 5,
            "device_channel": 0,
            "station_sn": "REDACTED",
            "schedule": "",
            "schedulex": "",
            "wifi_mac": "REDACTED",
            "main_sw_version": "2.157",
            "main_hw_version": "P2",
            "sec_sw_version": "1.030",
            "sec_hw_version": "P2",
            "sector_id": 0,
            "event_num": 26,
            "wifi_ssid": "REDACTED",
            "ip_addr": "REDACTED",
            "volume": "Anker_p988CTsnH",
            "main_sw_time": 1562640644,
            "bind_time": 1561916617,
            "bt_mac": "8C858013A8DE",
            "create_time": 1557986947,
            "update_time": 1563085853,
            "status": 1,
            "svr_domain": "",
            "svr_port": 0,
            "station_conn": {
                "station_sn": "REDACTED",
                "station_name": "Doorbell",
                "station_model": "T8200",
                "main_sw_version": "2.157",
                "main_hw_version": "P2",
                "p2p_did": "REDACTED",
                "push_did": "REDACTED",
                "ndt_did": "REDACTED",
                "p2p_conn": "REDACTED",
                "app_conn": "REDACTED",
                "binded": false,
                "setup_code": ""
            },
            "family_num": 0,
            "member": {
                "family_id": REDACTED,
                "station_sn": "REDACTED",
                "admin_user_id": "REDACTED",
                "member_user_id": "REDACTED",
                "member_type": 2,
                "permissions": 0,
                "member_nick": "",
                "action_user_id": "REDACTED",
                "fence_state": 0,
                "create_time": 1561916618,
                "update_time": 1561916618,
                "status": 1,
                "email": "youremail@domain.tld",
                "nick_name": "youremail",
                "avatar": "",
                "action_user_name": "youremail"
            },
            "permission": null,
            "params": [
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2031,
                    "param_value": "3",
                    "create_time": 1561916890,
                    "update_time": 1561916890,
                    "status": 1
                },
                {
                    "param_id": 1263342,
                    "device_sn": "REDACTED",
                    "param_type": 2015,
                    "param_value": "true",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2030,
                    "param_value": "0",
                    "create_time": 1561916861,
                    "update_time": 1561916861,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2006,
                    "param_value": "{\"polygonArray\":[{\"pointArray\":[{\"x\":256,\"y\":262},{\"x\":1294,\"y\":213},{\"x\":2091,\"y\":278},{\"x\":2050,\"y\":1055},{\"x\":1234,\"y\":1187},{\"x\":310,\"y\":1148}]}]}",
                    "create_time": 1562475264,
                    "update_time": 1562475264,
                    "status": 1
                },
                {
                    "param_id": 1263345,
                    "device_sn": "REDACTED",
                    "param_type": 2003,
                    "param_value": "148",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2033,
                    "param_value": "1",
                    "create_time": 1561916881,
                    "update_time": 1561916881,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 1134,
                    "param_value": "0",
                    "create_time": 1561916751,
                    "update_time": 1561916751,
                    "status": 1
                },
                {
                    "param_id": 1263346,
                    "device_sn": "REDACTED",
                    "param_type": 2022,
                    "param_value": "74",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 1263341,
                    "device_sn": "REDACTED",
                    "param_type": 2002,
                    "param_value": "true",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 1263344,
                    "device_sn": "REDACTED",
                    "param_type": 2005,
                    "param_value": "1",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2028,
                    "param_value": "6",
                    "create_time": 1561917067,
                    "update_time": 1561917067,
                    "status": 1
                },
                {
                    "param_id": 1263340,
                    "device_sn": "REDACTED",
                    "param_type": 2001,
                    "param_value": "true",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 1133,
                    "param_value": "0",
                    "create_time": 1561916751,
                    "update_time": 1561916751,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2010,
                    "param_value": "{\"totalCapcity\":4294967296,\"usedCapcity\":314370867}",
                    "create_time": 1561917086,
                    "update_time": 1561917086,
                    "status": 1
                },
                {
                    "param_id": 0,
                    "device_sn": "REDACTED",
                    "param_type": 2029,
                    "param_value": "1",
                    "create_time": 1561916883,
                    "update_time": 1561916883,
                    "status": 1
                },
                {
                    "param_id": 1263343,
                    "device_sn": "REDACTED",
                    "param_type": 2004,
                    "param_value": "1",
                    "create_time": 1561916618,
                    "update_time": 1561916618,
                    "status": 1
                }
            ],
            "pir_total": 3,
            "pir_none": 0,
            "week_pir_total": 24,
            "week_pir_none": 0,
            "month_pir_total": 48,
            "month_pir_none": 0
        }
    ]
}
```
## Get History
POST `https://mysecurity.eufylife.com/api/v1/event/app/get_all_history_record`

Headers:

`x-auth-token: AUTH_TOKEN_HERE`

Body:
```
{
	"device_sn": "",
	"end_time": 0,
	"id": 0,
	"num": 100,
	"offset": -14400,
	"pullup": true,
	"shared": true,
	"start_time": 0,
	"storage": 0
}
```

Response
```
{
    "code": 0,
    "msg": "Succeed.",
    "data": [
        {
            "monitor_id": REDACTED,
            "station_sn": "REDACTED",
            "device_sn": "REDACTED",
            "storage_type": 1,
            "storage_path": "/mnt/userdata/video/h264_video_20190713_222945.data",
            "hevc_storage_path": "",
            "cloud_path": "",
            "frame_num": 481,
            "thumb_path": "https://zhixin-security-pr.s3.us-west-2.amazonaws.com/thumb/2019/07/14/station/REDACTED",
            "thumb_data": "",
            "start_time": 1563071383447,
            "end_time": 1563071415402,
            "cipher_id": 128,
            "cipher_user_id": "REDACTED",
            "has_human": 1,
            "volume": "Anker_p988CTsnH",
            "vision": 0,
            "device_name": "Doorbell",
            "device_type": 5,
            "video_type": 1003,
            "viewed": false,
            "create_time": 1563071417,
            "update_time": 1563071417,
            "status": 1,
            "station_name": "",
            "p2p_did": "REDACTED",
            "push_did": "REDACTED",
            "p2p_license": "REDACTED",
            "push_license": "REDACTED",
            "ndt_did": "REDACTED",
            "ndt_license": "REDACTED",
            "p2p_conn": "REDACTED",
            "app_conn": "REDACTED",
            "wipn_enc_dec_key": "REDACTED",
            "wipn_ndt_aes128key": "REDACTED",
            "query_server_did": "REDACTED",
            "prefix": "",
            "ai_faces": null,
            "is_favorite": false
        },
        [...]
}
```
## Start Stream (returns an RTMP URL)
POST `https://mysecurity.eufylife.com/api/v1/web/equipment/start_stream`

Headers:

`x-auth-token: AUTH_TOKEN_HERE`

Body:
```
{
	"device_sn": "REDACTED", 
    "station_sn": "REDACTED", 
    "proto": 2
}
```

Response
```
{
    "code": 0,
    "msg": "Succeed.",
    "data": {
        "url": "rtmp://p2p-vir-7.eufylife.com/hls/REDACTED=?time=1563126670&token=REDACTED"
    }
}
```
