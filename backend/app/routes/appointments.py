from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.services.appointment_service import book_appointment

appointments_bp = Blueprint(
    "appointments",
    __name__,
    url_prefix="/appointments"
)


@appointments_bp.route("/book", methods=["POST"])
@jwt_required()
def book():
    data = request.json

    doctor_id = data.get("doctor_id")
    requested_time = data.get("requested_time")

    if not doctor_id or not requested_time:
        return {"error": "doctor_id and requested_time required"}, 400

    try:
        requested_time = datetime.fromisoformat(requested_time)
    except ValueError:
        return {"error": "Invalid datetime format"}, 400

    patient_id = get_jwt_identity()

    return book_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        requested_time=requested_time
    )
