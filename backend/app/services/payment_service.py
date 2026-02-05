from app.database.db import db
from datetime import datetime
from app.database.models import Bill, Payment


def mark_bill_paid(bill_id, transaction_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return None

    bill.status = "paid"
    db.session.commit()


def pay_bill(bill_id, payment_method):
    bill = Bill.query.get(bill_id)
    if not bill:
        return {"error": "Bill not found"}, 404

    if bill.status == "paid":
        return {"error": "Bill already paid"}, 400

    payment = Payment(
        bill_id=bill.id,
        transaction_id=f"TXN-{bill.id}-{int(datetime.utcnow().timestamp())}",
        payment_method=payment_method,
        amount=bill.total_amount,
        status="success",
    )

    bill.status = "paid"

    db.session.add(payment)
    db.session.commit()

    return {
        "message": "Payment successful",
        "bill_id": bill.id,
        "amount": bill.total_amount,
    }
