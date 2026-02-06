from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.db import db
from app.database.models import DoctorProfile

doctor_bp = Blueprint("doctors", __name__, url_prefix="/doctors")


@doctor_bp.route("/", methods=["GET"])
def list_doctors():
    doctors = DoctorProfile.query.all()
    return {"doctors": [
        {
            "user_id": d.user_id,
            "name": d.name,
            "specialization": d.specialization,
            "experience_years": d.experience_years,
        }
        for d in doctors
    ]}


# ✅ THIS WAS MISSING
@doctor_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_doctor_profile():
    data = request.json
    user_id = get_jwt_identity()  # take from JWT, NOT from client

    doctor = DoctorProfile(
        user_id=user_id,
        name=data.get("name"),
        specialization=data.get("specialization"),
        experience_years=data.get("experience_years"),
    )

    db.session.add(doctor)
    db.session.commit()

    return {"message": "Doctor profile created"}, 201

@doctor_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_doctor_profile():
    user_id = get_jwt_identity()

    doctor = DoctorProfile.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"error": "Profile not found"}, 404

    return {
        "user_id": doctor.user_id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "experience_years": doctor.experience_years
    }
