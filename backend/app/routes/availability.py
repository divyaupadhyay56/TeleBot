from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.database.db import db
from app.database.models import DoctorProfile, DoctorAvailability

availability_bp = Blueprint(
    "availability", __name__, url_prefix="/doctors/availability"
)

@availability_bp.route("/", methods=["POST"])
@jwt_required()
def add_availability():
    user_id = get_jwt_identity()
    data = request.json

    doctor = DoctorProfile.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"error": "Doctor profile not found"}, 404

    date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    start_time = datetime.strptime(data["start_time"], "%H:%M").time()
    end_time = datetime.strptime(data["end_time"], "%H:%M").time()

    if start_time >= end_time:
        return {"error": "Invalid time range"}, 400

    # 🔴 Overlap check
    overlap = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor.user_id,
        DoctorAvailability.date == date,
        DoctorAvailability.is_active == True,
        DoctorAvailability.start_time < end_time,
        DoctorAvailability.end_time > start_time
    ).first()

    if overlap:
        return {"error": "Overlapping slot exists"}, 400

    slot = DoctorAvailability(
        doctor_id=doctor.user_id,
        date=date,
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(slot)
    db.session.commit()

    return {"message": "Availability added"}, 201
