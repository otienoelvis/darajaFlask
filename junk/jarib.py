from flask import Flask
from flask import request
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app = Flask(__name__)
consumer_key = "H0JqRdy0oWqnJY60gGosulCGIqLfJjbd"
consumer_secret = "LiNqvVvLQ7ZBTdDk"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
base_url = "https://18.224.195.36:3000"

d = datetime.now()
timestamp = d.strftime("%Y%m%d%H%M%S")

datatoEncode = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"+timestamp
encoded = base64.b64encode(datatoEncode.encode())
decoded_pass = encoded.decode("utf-8")



@app.route("/")
def home():
    return "hello there"


@app.route("/access_token")
def token():
    data = acc_token()
    return data


@app.route("/register_url")
def register_url():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    # 174379
    response_data = requests.post(
        mpesa_endpoint,
        json={
            "ShortCode": "603021",
            "ResponseType": "Completed",
            "ConfirmationURL": "https://18.224.195.36:3000/c2b/confirm",
            "ValidationURL": "https://18.224.195.36:3000/c2b/validation"
        },
        headers=headers
    )

    return response_data.json()


@app.route("/c2b")
def simulate_c2b():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    request = {
        "ShortCode": "603021",
        "CommandID": "CustomerPayBillOnline",
        "Amount": "1",
        "Msisdn": "254708374149",
        "BillRefNumber": "12345678"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.json())
    return response.json()


@app.route("/c2b/confirm")
def confirm():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("confirm.json", "a") as f:
        json.dump(data, f, indent=2)


@app.route("/c2b/validation")
def validate():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("validate.json", "a") as f:
        json.dump(data, f, indent=2)


@app.route("/mpesaOnline")
def simulate_online():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    request = {
        "BusinessShortCode": "174379",
        "Password": decoded_pass,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "254745914885",
        "PartyB": "174379",
        "PhoneNumber": "254745914885",
        "CallBackURL": "https.fullstackdjango.com/lipanampesa",
        "AccountReference": "12345678",
        "TransactionDesc": "pay fees",

    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.json())
    return response.json()


def acc_token():
    data = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()

    # with open("access_token.json", "w") as f:
    #  json.dump(data, f, indent=2)

    return data["access_token"]


if __name__ == '__main__':
    app.run("0.0.0.0", port=3000, debug=True)
