from flask import Blueprint
from app.services.pharmacy_service import get_all_pharmacies, get_pharmacy_by_id

pharmacy_bp = Blueprint("pharmacies", __name__, url_prefix="/pharmacies")


@pharmacy_bp.route("/", methods=["GET"])
def list_pharmacies():
    return {"pharmacies": get_all_pharmacies()}


@pharmacy_bp.route("/<int:user_id>", methods=["GET"])
def pharmacy_profile(user_id):
    pharmacy = get_pharmacy_by_id(user_id)
    if not pharmacy:
        return {"error": "Pharmacy not found"}, 404

    return pharmacy
