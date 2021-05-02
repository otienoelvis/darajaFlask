from daraja import config
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import json

api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


def acc_token():
    data = requests.get(api_URL, auth=HTTPBasicAuth(config.consumer_key, config.consumer_secret)).json()

    return data["access_token"]


def timestamp():
    d = datetime.now()
    timestamp = d.strftime("%Y%m%d%H%M%S")

    return timestamp


def decoded_pass():
    datatoEncode = config.BusinessShortCode + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + timestamp()
    encoded = base64.b64encode(datatoEncode.encode())
    decoded_pass = encoded.decode("utf-8")

    return decoded_pass
