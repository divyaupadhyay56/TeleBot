from app.database.db import db
from app.database.models import Bill, BillItem

def generate_appointment_bill(patient_id, appointment_id):
    CONSULTATION_FEE = 500

    bill = Bill(
        patient_id=patient_id,
        appointment_id=appointment_id,
        total_amount=CONSULTATION_FEE
    )
    db.session.add(bill)
    db.session.flush()

    item = BillItem(
        bill_id=bill.id,
        description="Doctor Consultation",
        amount=CONSULTATION_FEE
    )
    db.session.add(item)
    db.session.commit()

    return bill




def generate_bill(patient_id, service_type, service_id, items):
    """
    items = [
        {"description": "Doctor Consultation", "amount": 500},
        {"description": "Emergency Charge", "amount": 800}
    ]
    """

    subtotal = sum(item["amount"] for item in items)
    tax = int(subtotal * 0.05)   # 5% example tax
    total = subtotal + tax

    bill = Bill(
        patient_id=patient_id,
        service_type=service_type,
        service_id=service_id,
        subtotal=subtotal,
        tax_amount=tax,
        total_amount=total
    )

    db.session.add(bill)
    db.session.flush()

    for item in items:
        db.session.add(
            BillItem(
                bill_id=bill.id,
                description=item["description"],
                amount=item["amount"]
            )
        )

    db.session.commit()
    return bill
