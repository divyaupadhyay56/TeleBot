from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.emergency_service import handle_emergency
from app.services.ambulance_service import call_ambulance

emergency_bp = Blueprint("emergency", __name__, url_prefix="/emergency")


@emergency_bp.route("/hospital", methods=["POST"])
@jwt_required()
def emergency_hospital():
    data = request.json
    return handle_emergency(
        patient_id=get_jwt_identity(), lat=data["lat"], lng=data["lng"]
    )


@emergency_bp.route("/ambulance", methods=["POST"])
@jwt_required()
def emergency_ambulance():
    data = request.json
    return call_ambulance(
        patient_id=get_jwt_identity(), lat=data["lat"], lng=data["lng"]
    )
