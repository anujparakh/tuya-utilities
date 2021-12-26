# Authorization key obtained from the cloud development project
import time
import requests
import json

client_id = 'ahe44xetab6lp4vyo8rc'
secret = 'b2f8b58488b24f8f8daffc1f7d415a6f'

# Call the APIs according to your region.
# China https://openapi.tuyacn.com
# America https://openapi.tuyaus.com
# Europe https://openapi.tuyaeu.com
# India https://openapi.tuyain.com

base = 'https://openapi.tuyaus.com'

# Signature algorithm function


def calc_sign(msg, key):
    import hmac
    import hashlib
    sign = hmac.new(msg=bytes(msg, 'latin-1'), key=bytes(key,
                    'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    return sign


t = str(int(time.time()*1000))
r = requests.get(base+'/v1.0/token?grant_type=1',
                 headers={
                     'client_id': client_id,
                     'sign': calc_sign(client_id+t, secret),
                     'secret': secret,
                     't': t,
                     'sign_method': 'HMAC-SHA256',
                 })

res = r.json()['result']

# get request function


def GET(url, headers={}):

    t = str(int(time.time()*1000))
    default_par = {
        'client_id': client_id,
        'access_token': res['access_token'],
        'sign': calc_sign(client_id+res['access_token']+t, secret),
        't': t,
        'sign_method': 'HMAC-SHA256',
    }
    r = requests.get(base + url, headers=dict(default_par, **headers))

    # Beautify the format of request result.
    beautified = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return beautified, r.json()

# post request function


def POST(url, headers={}, body={}):
    import json
    t = str(int(time.time()*1000))

    default_par = {
        'client_id': client_id,
        'access_token': res['access_token'],
        'sign': calc_sign(client_id+res['access_token']+t, secret),
        't': t,
        'sign_method': 'HMAC-SHA256',
    }
    r = requests.post(base + url, headers=dict(default_par,
                      **headers), data=json.dumps(body))

    # Beautify the format of request result.
    r = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return r


_, jsonResult = GET(url=f'/v1.0/iot-01/associated-users/devices?last_row_key=')

i = 1
print("--------------------------")
for device in jsonResult["result"]["devices"]:
    print("Device ", i, ": ", device["name"])
    print("ID: ", device["id"])
    print("Local Key: ", device["local_key"])
    print("--------------------------")
    i += 1
