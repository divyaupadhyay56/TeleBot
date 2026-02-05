import razorpay
import os

from app.database.db import db
from app.database.models import Payment, Bill

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


def verify_payment(data):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
    except:
        return {"error": "Signature verification failed"}, 400

    payment = Payment.query.filter_by(
        razorpay_order_id=data["razorpay_order_id"]
    ).first()

    if not payment:
        return {"error": "Payment record not found"}, 404

    payment.razorpay_payment_id = data["razorpay_payment_id"]
    payment.razorpay_signature = data["razorpay_signature"]
    payment.status = "success"

    bill = Bill.query.get(payment.bill_id)
    bill.status = "paid"

    db.session.commit()

    return {"message": "Payment verified successfully"}
