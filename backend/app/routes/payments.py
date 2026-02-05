from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.payment_service import pay_bill
from app.services.razorpay_service import create_razorpay_order
from app.services.payment_verify_service import verify_payment
payment_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payment_bp.route("/pay", methods=["POST"])
@jwt_required()
def pay():
    data = request.json
    bill_id = data.get("bill_id")
    method = data.get("payment_method", "online")

    if not bill_id:
        return {"error": "bill_id required"}, 400

    return pay_bill(bill_id, method)

@payment_bp.route("/razorpay/create-order", methods=["POST"])
@jwt_required()
def create_order():
    bill_id = request.json.get("bill_id")
    if not bill_id:
        return {"error": "bill_id required"}, 400

    order = create_razorpay_order(bill_id)
    if not order:
        return {"error": "Invalid bill"}, 400

    return order


# 🔹 Verify payment after frontend success
@payment_bp.route("/razorpay/verify", methods=["POST"])
@jwt_required()
def verify():
    return verify_payment(request.json)