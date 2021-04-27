import requests
from requests.auth import HTTPBasicAuth
import json

# second function


consumer_key = "H0JqRdy0oWqnJY60gGosulCGIqLfJjbd"
consumer_secret = "LiNqvVvLQ7ZBTdDk"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


def access_token():
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()

    with open("access_token.json", "w") as f:
        json.dump(data, f, indent=2)

    print(data)
    return data["access_token"]


if __name__ == '__main__':
    access_token()
