from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import Bill, BillItem

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")


# 🔹 View bill details
@billing_bp.route("/<int:bill_id>", methods=["GET"])
@jwt_required()
def get_bill(bill_id):
    user_id = get_jwt_identity()
    bill = Bill.query.get_or_404(bill_id)

    if bill.patient_id != user_id:
        return {"error": "Unauthorized"}, 403

    items = BillItem.query.filter_by(bill_id=bill.id).all()

    return {
        "bill_id": bill.id,
        "service_type": bill.service_type,
        "subtotal": bill.subtotal,
        "tax": bill.tax_amount,
        "total": bill.total_amount,
        "status": bill.status,
        "items": [{"description": i.description, "amount": i.amount} for i in items],
    }
