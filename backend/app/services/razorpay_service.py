import razorpay
import os

from app.database.db import db
from app.database.models import Bill, Payment

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


def create_razorpay_order(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill or bill.status != "unpaid":
        return None

    order = client.order.create({
        "amount": bill.total_amount * 100,  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment(
        bill_id=bill.id,
        razorpay_order_id=order["id"],
        amount=bill.total_amount,
        status="created"
    )

    db.session.add(payment)
    db.session.commit()

    return {
        "order_id": order["id"],
        "amount": bill.total_amount,
        "currency": "INR",
        "razorpay_key": os.getenv("RAZORPAY_KEY_ID")
    }
