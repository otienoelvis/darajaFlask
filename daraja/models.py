from datetime import datetime
from daraja import db
import pytz


class TranscComplete(db.Model):
    MerchantRequestID = db.Column(db.String, primary_key=True, autoincrement=False)
    CheckoutRequestID = db.Column(db.String, unique=True)
    ResultCode = db.Column(db.Integer, nullable=False)
    ResultDesc = db.Column(db.String, unique=True, nullable=False)

    Amount = db.Column(db.Float, nullable=False)
    MpesaReceiptNumber = db.Column(db.String, unique=True)
    Balance = db.Column(db.Float, nullable=False, default=0.0)  # add the amount paid
    TransactionDate = db.Column(db.DateTime, nullable=False)
    PhoneNumber = db.Column(db.Integer, nullable=False)

    DateAdded = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    def __repr__(self):
        return f"TranscComplete('{self.MerchantRequestID}', '{self.CheckoutRequestID}', '{self.ResultCode}', " \
               f"'{self.ResultDesc}', '{self.DateAdded}')"


class TranscUncomplete(db.Model):
    MerchantRequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CheckoutRequestID = db.Column(db.String(50), unique=True)
    ResultCode = db.Column(db.Boolean, nullable=False)
    ResultDesc = db.Column(db.String(25), unique=True, nullable=False)
    DateAdded = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    def __repr__(self):
        return f"TranscUncomplete('{self.MerchantRequestID}', '{self.CheckoutRequestID}', '{self.ResultCode}', " \
               f"'{self.ResultDesc}', '{self.DateAdded}')"
