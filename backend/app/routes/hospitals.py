from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.database.db import db
from app.database.models import Hospital

hospitals_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")


# ✅ CREATE HOSPITAL
@hospitals_bp.route("", methods=["POST"])
@jwt_required()   # optional: remove if you want public creation
def create_hospital():
    data = request.json

    name = data.get("name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not name:
        return {"error": "Hospital name is required"}, 400

    if Hospital.query.filter_by(name=name).first():
        return {"error": "Hospital already exists"}, 400

    hospital = Hospital(
        name=name,
        latitude=latitude,
        longitude=longitude
    )

    db.session.add(hospital)
    db.session.commit()

    return {
        "message": "Hospital created successfully",
        "hospital": {
            "name": hospital.name,
            "latitude": hospital.latitude,
            "longitude": hospital.longitude
        }
    }, 201


# ✅ GET HOSPITAL PROFILE
@hospitals_bp.route("/<string:name>", methods=["GET"])
def get_hospital(name):
    hospital = Hospital.query.filter_by(name=name).first()
    if not hospital:
        return {"error": "Hospital not found"}, 404

    return {
        "name": hospital.name,
        "latitude": hospital.latitude,
        "longitude": hospital.longitude
    }, 200
