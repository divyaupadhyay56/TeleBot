from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.db import db
from app.database.models import PharmacyProfile, UserRole, Role
from app.services.pharmacy_service import find_nearby_pharmacies

pharmacy_bp = Blueprint("pharmacies", __name__, url_prefix="/pharmacies")


# 🔹 CREATE PHARMACY PROFILE
@pharmacy_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_pharmacy_profile():
    user_id = get_jwt_identity()

    role = (
        db.session.query(Role.name)
        .join(UserRole)
        .filter(UserRole.user_id == user_id)
        .scalar()
    )

    if role != "pharmacy":
        return {"error": "Forbidden"}, 403

    if PharmacyProfile.query.filter_by(user_id=user_id).first():
        return {"error": "Profile already exists"}, 400

    data = request.json

    profile = PharmacyProfile(
        user_id=user_id,
        store_name=data.get("store_name"),
        license_number=data.get("license_number"),
        home_delivery_available=data.get("home_delivery_available", False),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    db.session.add(profile)
    db.session.commit()

    return {"message": "Pharmacy profile created"}, 201


# 🔹 GET MY PROFILE
@pharmacy_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_pharmacy_profile():
    user_id = get_jwt_identity()

    profile = PharmacyProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return {"error": "Profile not found"}, 404

    return {
        "user_id": profile.user_id,
        "store_name": profile.store_name,
        "license_number": profile.license_number,
        "home_delivery_available": profile.home_delivery_available,
        "latitude": profile.latitude,
        "longitude": profile.longitude
    }


# 🔹 FIND NEARBY PHARMACIES
@pharmacy_bp.route("/nearby", methods=["GET"])
@jwt_required()
def nearby_pharmacies():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    radius = request.args.get("radius_km", default=5, type=float)

    if lat is None or lng is None:
        return {"error": "lat and lng required"}, 400

    return {
        "pharmacies": find_nearby_pharmacies(lat, lng, radius)
    }, 200