from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.models import DoctorProfile
from app.database.db import db

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")

@doctors_bp.route("/profile", methods=["GET"])
@jwt_required()
def doctor_profile():
    user_id = get_jwt_identity()

    doctor = DoctorProfile.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"error": "Doctor profile not found"}, 404

    return {
        "name": doctor.name,
        "specialization": doctor.specialization,
        "experience_years": doctor.experience_years,
        "hospital_name": doctor.hospital_name,
        "hospital_location": {
            "latitude": doctor.hospital.latitude if doctor.hospital else None,
            "longitude": doctor.hospital.longitude if doctor.hospital else None,
        }
    }, 200