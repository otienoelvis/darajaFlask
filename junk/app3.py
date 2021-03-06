from flask import Flask
from flask import request
import requests

from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)
consumer_key = "H0JqRdy0oWqnJY60gGosulCGIqLfJjbd"
consumer_secret = "LiNqvVvLQ7ZBTdDk"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
base_url = "154.123.168.169:36662"


@app.route("/home")
def home():
    return "hello there"


@app.route("/access_token")
def token():
    data = acc_token()
    return data


@app.route("/register_url")
def register_url():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % acc_token()}
    req = {
        "ShortCode": "603021",
        "ResponseType": "Completed",
        "ConfirmationURL": "",
        "ValidationURL": ""
    }
    response = requests.post(api_url, json=req, headers=headers)

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


def acc_token():
    data = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()

    with open("../access_token.json", "w") as f:
        json.dump(data, f, indent=2)

    return data["access_token"]


if __name__ == '__main__':
    app.run("0.0.0.0", port=3000, debug=True)
