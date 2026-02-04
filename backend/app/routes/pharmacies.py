from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.pharmacy_service import get_all_pharmacies, get_pharmacy_profile, find_nearby_pharmacies

pharmacy_bp = Blueprint("pharmacies", __name__, url_prefix="/pharmacies")


@pharmacy_bp.route("/", methods=["GET"])
def list_pharmacies():
    return {"pharmacies": get_all_pharmacies()}


@pharmacy_bp.route("/<int:user_id>", methods=["GET"])
def pharmacy_profile(user_id):
    pharmacy = get_pharmacy_profile(user_id)
    if not pharmacy:
        return {"error": "Pharmacy not found"}, 404

    return pharmacy

# 🔹 Find nearby pharmacies (for map)
@pharmacy_bp.route("/nearby", methods=["POST"])
@jwt_required()
def nearby_pharmacies():
    data = request.json

    lat = data.get("lat")
    lng = data.get("lng")
    radius = data.get("radius_km", 5)

    if lat is None or lng is None:
        return {"error": "lat and lng required"}, 400

    return {
        "pharmacies": find_nearby_pharmacies(lat, lng, radius)
    }