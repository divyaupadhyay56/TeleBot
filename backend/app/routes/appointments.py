from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.db import db
from app.database.models import Appointment, DoctorAvailability

appointment_bp = Blueprint(
    "appointments", __name__, url_prefix="/appointments"
)


@appointment_bp.route("/", methods=["POST"])
@jwt_required()
def book_appointment():
    patient_id = get_jwt_identity()
    data = request.json

    availability_id = data.get("availability_id")
    if not availability_id:
        return {"error": "availability_id is required"}, 400

    # 1️⃣ Check slot exists & active
    slot = DoctorAvailability.query.filter_by(
        id=availability_id,
        is_active=True
    ).first()

    if not slot:
        return {"error": "Slot not available"}, 404

    # 2️⃣ Check if already booked
    existing = Appointment.query.filter_by(
        availability_id=slot.id
    ).first()

    if existing:
        # 3️⃣ Suggest alternatives
        alternatives = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == slot.doctor_id,
            DoctorAvailability.date == slot.date,
            DoctorAvailability.is_active == True,
            DoctorAvailability.id != slot.id
        ).all()

        return {
            "error": "Slot already booked",
            "alternatives": [
                {
                    "availability_id": s.id,
                    "start_time": s.start_time.strftime("%H:%M"),
                    "end_time": s.end_time.strftime("%H:%M")
                }
                for s in alternatives
            ]
        }, 400

    # 4️⃣ Book appointment
    appointment = Appointment(
        doctor_id=slot.doctor_id,
        patient_id=patient_id,
        availability_id=slot.id
    )

    db.session.add(appointment)
    db.session.commit()

    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    }, 201
