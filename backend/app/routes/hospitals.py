from flask import Blueprint, jsonify, request
from app.services.hospital_service import get_all_hospitals, get_hospital_by_id, create_hospital
from app.database.models import Hospital, DoctorProfile

hospital_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")


@hospital_bp.route("/", methods=["POST"])
def create_hospital_route():
    data = request.json

    if not data.get("name"):
        return {"error": "Hospital name is required"}, 400

    hospital = create_hospital(data)
    return hospital, 201


@hospital_bp.route("/<int:hospital_id>", methods=["GET"])
def hospital_profile(hospital_id):
    hospital = get_hospital_by_id(hospital_id)
    if not hospital:
        return {"error": "Hospital not found"}, 404

    return hospital
@hospital_bp.route("/<int:hospital_id>/doctors", methods=["GET"])
def get_doctors_by_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)

    if not hospital:
        return {"error": "Hospital not found"}, 404

    doctors = DoctorProfile.query.filter_by(
        hospital_id=hospital_id
    ).all()

    return jsonify([
        {
            "user_id": d.user_id,
            "name": d.name,
            "specialization": d.specialization,
            "experience_years": d.experience_years
        }
        for d in doctors
    ])