from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.models import PatientProfile

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")

@patients_bp.route("/profile", methods=["GET"])
@jwt_required()
def patient_profile():
    user_id = get_jwt_identity()

    patient = PatientProfile.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"error": "Patient profile not found"}, 404

    return {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "blood_group": patient.blood_group,
    }, 200