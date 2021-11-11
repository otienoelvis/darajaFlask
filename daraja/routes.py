from flask import request, jsonify, Response
from daraja import app, config, db
import requests
from daraja.utils import acc_token, timestamp, decoded_pass
import json
from daraja.models import TranscComplete, TranscUncomplete
from datetime import datetime

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
            "ShortCode": config.shortCode,
            "ResponseType": "Canceled",
            "ConfirmationURL": f"{config.base_url}/c2b/confirm",
            "ValidationURL": f"{config.base_url}/c2b/validation"
        },
        headers=headers
    )

    return response_data.json()


@app.route("/mpesaOnline", methods=["POST", "GET"])
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
        "CallBackURL": f"{config.base_url}/lipanampesa",
        "AccountReference": "Oty",
        "TransactionDesc": "Oty"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return response.json()


@app.route("/lipanampesa", methods=["POST", "GET"])
def process_lipanampesa():
    """
    callback url, receives data from mpesaOnline
    :return:
    """
    data = request.get_json()
    if data["Body"]["stkCallback"]["ResultCode"] != 1032:
        TranscDate = str(data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"])
        TransactionDate = datetime.strptime(TranscDate, "%Y%m%d%H%M%S")

        transc = TranscComplete(MerchantRequestID=data["Body"]["stkCallback"]["MerchantRequestID"],
                                CheckoutRequestID=data["Body"]["stkCallback"]["CheckoutRequestID"],
                                ResultCode=data["Body"]["stkCallback"]["ResultCode"],
                                ResultDesc=data["Body"]["stkCallback"]["ResultDesc"],
                                Amount=data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"],
                                MpesaReceiptNumber=data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"],
                                Balance=0.0,
                                TransactionDate=TransactionDate,
                                PhoneNumber=data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
                                )

        db.session.add(transc)
        db.session.commit()
    else:
        print("Request cancelled by user")

    return data


@app.route("/c2b")
def simulate_c2b():
    """
    send to pay bill from stk
    :return:
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    request = {
        "ShortCode": config.shortCode,
        "CommandID": "CustomerPayBillOnline",
        "Amount": "100",
        "Msisdn": config.test_msisdn,
        "BillRefNumber": "12345678"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return response.json()


@app.route("/c2b/confirm", methods=['POST', 'GET'])
def confirm():
    """get data"""
    data = request.get_json()
    """write to file"""
    with open("confirm.json", "w") as f:
        json.dump(data, f, indent=2)

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }


@app.route("/c2b/validation", methods=['POST', 'GET'])
def validate():
    """get data"""
    data = request.get_json()
    """write to file"""

    with open("validate.json", "w") as f:
        json.dump(data, f, indent=2)

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
        "ThirdPartyTransID": "Otyyy"
    }
