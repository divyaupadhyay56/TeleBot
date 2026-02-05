from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.medicine_service import search_medicine

medicine_bp = Blueprint("medicines", __name__, url_prefix="/medicines")


@medicine_bp.route("/search", methods=["POST"])
@jwt_required()
def search():
    data = request.json

    medicine_name = data.get("medicine_name")
    lat = data.get("lat")
    lng = data.get("lng")
    radius = data.get("radius_km", 5)

    if not medicine_name or lat is None or lng is None:
        return {"error": "medicine_name, lat, lng required"}, 400

    results = search_medicine(
        medicine_name=medicine_name, user_lat=lat, user_lng=lng, radius_km=radius
    )

    if not results:
        return {"message": "Medicine not available nearby", "results": []}

    return {"medicine": medicine_name, "results": results}
