import json
from daraja import db
from daraja.models import TranscComplete, TranscUncomplete
from datetime import datetime


def process_lipanampesa():
    with open("../daraja/lipanampesa.json", "r") as f:
        data = json.load(f)

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

process_lipanampesa()
