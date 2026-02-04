from flask import Blueprint
from app.services.hospital_service import get_all_hospitals, get_hospital_by_id

hospital_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")


@hospital_bp.route("/", methods=["GET"])
def list_hospitals():
    return {"hospitals": get_all_hospitals()}


@hospital_bp.route("/<int:hospital_id>", methods=["GET"])
def hospital_profile(hospital_id):
    hospital = get_hospital_by_id(hospital_id)
    if not hospital:
        return {"error": "Hospital not found"}, 404

    return hospital
