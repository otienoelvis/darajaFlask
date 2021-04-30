import requests
from requests.auth import HTTPBasicAuth
import json


consumer_key = "H0JqRdy0oWqnJY60gGosulCGIqLfJjbd"
consumer_secret = "LiNqvVvLQ7ZBTdDk"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
base_url = "https:3.12.118.35:5000"

data = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()

with open("access_token.json", "w") as f:
    json.dump(data, f, indent=2)

acc_token = data["access_token"]



def reg():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % acc_token}
    request = {"ShortCode": "60302ll",
               "ResponseType": "Completed",
               "ConfirmationURL": "https://fullstackdjango.com/confirmation",
               "ValidationURL": "https://fullstackdjango.com/validation"}

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


if __name__ == '__main__':
    reg()
