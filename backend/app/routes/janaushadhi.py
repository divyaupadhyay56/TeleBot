from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.janaushadhi_service import find_nearby_kendras

janaushadhi_bp = Blueprint(
    "janaushadhi",
    __name__,
    url_prefix="/janaushadhi"
)


@janaushadhi_bp.route("/nearby", methods=["POST"])
@jwt_required()
def nearby():
    data = request.json
    lat = data.get("lat")
    lng = data.get("lng")
    radius = data.get("radius_km", 5)

    if lat is None or lng is None:
        return {"error": "lat and lng required"}, 400

    return {
        "kendras": find_nearby_kendras(lat, lng, radius)
    }
