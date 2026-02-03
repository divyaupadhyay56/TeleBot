from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import PharmacyProfile

pharmacies_bp = Blueprint("pharmacies", __name__, url_prefix="/pharmacies")


@pharmacies_bp.route("/profile", methods=["GET"])
@jwt_required()
def pharmacy_profile():
    user_id = get_jwt_identity()

    pharmacy = PharmacyProfile.query.filter_by(user_id=user_id).first()
    if not pharmacy:
        return {"error": "Pharmacy profile not found"}, 404

    return {
        "store_name": pharmacy.store_name,
        "license_number": pharmacy.license_number,
    }, 200
