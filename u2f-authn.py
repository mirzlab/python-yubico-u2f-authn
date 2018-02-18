import time
import json
import argparse
import sys
import requests

from u2flib_host import u2f, exc
from u2flib_host.constants import APDU_USE_NOT_SATISFIED
from u2flib_host.utils import u2str
from u2flib_host.yubicommon.compat import text_type

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

def serverCall(serverUrl, method, params):
    if (params is not None):
        response = requests.get(serverUrl + "/" + method, params=params)
    else:
        response = requests.get(serverUrl + "/" + method)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(e.response.text, response=e.response)
    return json.loads(response.text)

def getAuthenticationRequestData():
    authenticationRequest = None
    while authenticationRequest is None:
        try:
            authenticationRequest = serverCall(serverUrl, "sign", None)
        except:
            authenticationRequest = None
            sys.stderr.write('\nAn error occured while retrieving server challenge. Retrying in 3.')
        time.sleep(3)
    # Get only what we need
    authenticationRequestData = authenticationRequest["registeredKeys"][0];
    authenticationRequestData["challenge"] = authenticationRequest["challenge"];
    return authenticationRequestData

def verifyAuthentication(device, authenticationRequestData):
    # Enumerate available devices
    sys.stdout.write('\nTouch the U2F device you wish to authenticate...\n')
    while 1:
        try:
            try:
                authenticateResponse = u2f.authenticate(device, json.dumps(authenticationRequestData), serverUrl)
                params = "data=" + json.dumps(authenticateResponse)
                verifyResponse = serverCall(serverUrl, "verify", params)
                return "counter" in verifyResponse
            except:
                pass
        except exc.APDUError as e:
            if e.code == APDU_USE_NOT_SATISFIED:
                pass
            else:
                return False
        except exc.DeviceError:
                return False
        time.sleep(0.25)

device = getDevice()
authenticationRequestData = getAuthenticationRequestData()
result = verifyAuthentication(device, authenticationRequestData)

if result:
    print "Authentication successful"
else:
    print "Authentication failed"
device.close()
