import time
import json
import argparse
import sys
import requests

from u2flib_host import u2f, exc
from u2flib_host.constants import APDU_USE_NOT_SATISFIED
from u2flib_host.utils import u2str
from u2flib_host.yubicommon.compat import text_type
from U2FClient import U2FClient

serverUrl = "http://localhost:8081";

def getDevice():
    devices = u2f.list_devices()
    if len(devices) != 1:
        sys.stderr.write('\nMore than one or no device detected. Exiting\n')
        sys.exit(1)

    device = None
    try:
        device = devices[0]
        device.open()
    except:
        pass
    return device

def serverCall(serverUrl, method, params, jsonFormat):
    if (params is not None):
        r = requests.get(serverUrl + "/" + method, params=params)
    else:
        r = requests.get(serverUrl + "/" + method)

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(e.response.text, response=e.response)
    if jsonFormat:
        return json.loads(r.text)
    else:
        return r.text

def getRegistrationRequestData():  
    registrationRequest = None
    while registrationRequest is None:
        try:
            registrationRequest = serverCall(serverUrl, "enroll", None, True)
        except:
            registrationRequest = None
            sys.stderr.write('\nAn error occured while retrieving server data. Retrying in 3.')
        time.sleep(3)
    # Get only what we need
    registrationRequestData = registrationRequest["registerRequests"][0];
    registrationRequestData["appId"] = registrationRequest["appId"];
    return registrationRequestData

def registerDevice(device, registrationRequestData):
    sys.stdout.write('\nTouch the U2F device you wish to register...\n')
    while 1:
        try:
            registerResponse = u2f.register(device, json.dumps(registrationRequestData), serverUrl)
            registerResponse["version"] = "U2F_V2"
            params = "data=" + json.dumps(registerResponse)
            bindResponse = serverCall(serverUrl, "bind", params, False)
            if bindResponse != "true":
                return False
            return True
        except exc.APDUError as e:
            if e.code == APDU_USE_NOT_SATISFIED:
                pass
            else:
                return False
        except:
                return False

        time.sleep(0.25)

device = getDevice()
registrationRequestData = getRegistrationRequestData()
result = registerDevice(device, registrationRequestData)

if result:
    print "Registration sucessful"
else:
    print "Registration failed"
device.close()

