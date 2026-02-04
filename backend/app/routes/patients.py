from flask import Blueprint
from app.services.patient_service import get_all_patients, get_patient_by_id

patient_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patient_bp.route("/", methods=["GET"])
def list_patients():
    return {"patients": get_all_patients()}


@patient_bp.route("/<int:user_id>", methods=["GET"])
def patient_profile(user_id):
    patient = get_patient_by_id(user_id)
    if not patient:
        return {"error": "Patient not found"}, 404

    return patient
