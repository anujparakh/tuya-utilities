# Utility functions to use tuya endpoints

# Authorization key obtained from the cloud development project
import time
import requests
import json
import datetime as dt


client_id = 'ahe44xetab6lp4vyo8rc'
secret = 'b2f8b58488b24f8f8daffc1f7d415a6f'

# Call the APIs according to your region.
# China https://openapi.tuyacn.com
# America https://openapi.tuyaus.com
# Europe https://openapi.tuyaeu.com
# India https://openapi.tuyain.com

base = 'https://openapi.tuyaus.com'  # America
token = []  # Filled with access token
lastRefreshed = time.time()

# Signature algorithm function


def calc_sign(msg, key):
    import hmac
    import hashlib
    sign = hmac.new(msg=bytes(msg, 'latin-1'), key=bytes(key,
                    'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    return sign

# get request function


def GET(url, headers={}):
    refreshTokenIfNeeded()
    t = str(int(time.time()*1000))
    default_par = {
        'client_id': client_id,
        'access_token': token['access_token'],
        'sign': calc_sign(client_id+token['access_token']+t, secret),
        't': t,
        'sign_method': 'HMAC-SHA256',
    }
    r = requests.get(base + url, headers=dict(default_par, **headers))

    # Beautify the format of request result.
    beautified = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return beautified, r.json()

# post request function


def POST(url, headers={}, body={}):
    refreshTokenIfNeeded()

    import json
    t = str(int(time.time()*1000))

    default_par = {
        'client_id': client_id,
        'access_token': token['access_token'],
        'sign': calc_sign(client_id+token['access_token']+t, secret),
        't': t,
        'sign_method': 'HMAC-SHA256',
    }
    r = requests.post(base + url, headers=dict(default_par,
                      **headers), data=json.dumps(body))

    # Beautify the format of request result.
    beautified = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return beautified, r.json()


def getAccessToken():
    t = str(int(time.time()*1000))
    r = requests.get(base+'/v1.0/token?grant_type=1',
                     headers={
                         'client_id': client_id,
                         'sign': calc_sign(client_id+t, secret),
                         'secret': secret,
                         't': t,
                         'sign_method': 'HMAC-SHA256',
                     })
    resp = r.json()['result']
    lastRefreshed = time.time()
    return resp


def getRefreshToken():
    t = str(int(time.time()*1000))
    r = requests.get(base+'/v1.0/token/'+res["refresh_token"],
                     headers={
                     'client_id': client_id,
                     'sign': calc_sign(client_id+t, secret),
                     'secret': secret,
                     't': t,
                     'sign_method': 'HMAC-SHA256',
                     })
    resp = r.json()['result']
    lastRefreshed = time.time()
    return resp


def refreshTokenIfNeeded():
    global token
    if(time.time() - lastRefreshed > token['expire_time']):
        token = getRefreshToken()


def getAllDevices():
    test, jsonResult = GET(
        url=f'/v1.0/iot-01/associated-users/devices?last_row_key=')
    return jsonResult


def getDevice(device_id):
    _, jsonResult = GET(url=f'/v1.0/devices/{device_id}')
    return jsonResult


def getDeviceFunctions(device_id):
    _, jsonResult = GET(url=f'/v1.0/devices/{device_id}/specifications')
    return jsonResult


def sendCommands(device_id, commands):
    return POST(url=f'/v1.0/devices/{device_id}/commands', body=commands)


def lightOnOff(device_id, isOn):
    return sendCommands(device_id, {"commands": [{"code": "switch_led", "value": isOn}]})

def toggleLight(device_id):
    deviceStatus = getDevice(device_id)["result"]["status"]
    for vals in deviceStatus:
        if vals["code"] == "switch_led":
            return lightOnOff(device_id, not vals["value"])

def setup():
    global token
    token = getAccessToken()


setup()

# TABLE LIGHTS: eb2adf5bf464095041agjf
# OFFICE LAMP TOP: eb44972f916fe8985b1svr
# OFFICE LAMP BOTTOM: eba3ca15657a474fabliaa
