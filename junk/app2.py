import json


def process_lipanampesa():
    with open("../daraja/lipanampesa.json", "r") as f:
        data = json.load(f)

        MerchantRequestID = data["Body"]["stkCallback"]["MerchantRequestID"]
        CheckoutRequestID = data["Body"]["stkCallback"]["CheckoutRequestID"]
        ResultCode = data["Body"]["stkCallback"]["ResultCode"]
        ResultDesc = data["Body"]["stkCallback"]["ResultDesc"]
        Amount = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        MpesaReceiptNumber = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        Balance = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
        TransactionDate = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        PhoneNumber = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]



process_lipanampesa()
