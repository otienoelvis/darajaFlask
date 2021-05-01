from flask import request
from daraja import app, config
import requests
from daraja.utils import acc_token, timestamp, decoded_pass
import json
#  from daraja.models import Site


api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


data = acc_token()
print(data)


@app.route("/")
@app.route("/home")
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
    response_data = requests.post(
        mpesa_endpoint,
        json={
            "ShortCode": config.ShortCode,
            "ResponseType": "Canceled",
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
        "ShortCode": config.ShortCode,
        "CommandID": "CustomerPayBillOnline",
        "Amount": "1",
        "Msisdn": "254708374149",
        "BillRefNumber": "123gh658"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return response.json()


@app.route("/c2b/confirm")
def confirm():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("confirm.json", "a") as f:
        json.dump(data, f, indent=2)
    return data


@app.route("/c2b/validation")
def validate():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("validate.json", "a") as f:
        json.dump(data, f, indent=2)
    return data


@app.route("/mpesaOnline")
def simulate_online():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    request = {
        "BusinessShortCode": config.BusinessShortCode,
        "Password": decoded_pass(),
        "Timestamp": timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "254745914885",
        "PartyB": "174379",
        "PhoneNumber": "254745914885",
        "CallBackURL": "http://18.224.195.36:3000/lipanampesa",
        "AccountReference": "Yooooooo",
        "TransactionDesc": "pay fees"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.json())
    return response.json()


@app.route("/lipanampesa", methods=["POST", "GET"])
def lipanampesa():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("lipanampesa.json", "a") as f:
        json.dump(data, f, indent=2)
    return data
