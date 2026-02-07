from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.patient_service import get_all_patients, get_patient_by_id
from app.database.db import db
from app.database.models import PatientProfile, UserRole, Role
patient_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patient_bp.route("/", methods=["GET"])
def list_patients():
    return {"patients": get_all_patients()}


@patient_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_patient_profile():
    user_id = get_jwt_identity()

    # role check
    role = (
        db.session.query(Role.name)
        .join(UserRole)
        .filter(UserRole.user_id == user_id)
        .scalar()
    )

    if role != "patient":
        return {"error": "Forbidden"}, 403

    if PatientProfile.query.filter_by(user_id=user_id).first():
        return {"error": "Profile already exists"}, 400

    data = request.json

    profile = PatientProfile(
        user_id=user_id,
        name=data.get("name"),
        age=data.get("age"),
        gender=data.get("gender"),
        blood_group=data.get("blood_group")
    )

    db.session.add(profile)
    db.session.commit()

    return {"message": "Patient profile created"}, 201


# 🔹 GET MY PROFILE
@patient_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_patient_profile():
    user_id = get_jwt_identity()

    profile = PatientProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return {"error": "Profile not found"}, 404

    return {
        "user_id": profile.user_id,
        "name": profile.name,
        "age": profile.age,
        "gender": profile.gender,
        "blood_group": profile.blood_group
    }

@patient_bp.route("/update-profile", methods=["PUT"])
@jwt_required()
def update_patient_profile():
    user_id = get_jwt_identity()

    profile = PatientProfile.query.get(user_id)
    if not profile:
        return {"error": "Patient profile not found"}, 404

    data = request.get_json()

    if "name" in data:
        profile.name = data["name"]
    if "age" in data:
        profile.age = data["age"]
    if "gender" in data:
        profile.gender = data["gender"]
    if "blood_group" in data:
        profile.blood_group = data["blood_group"]

    db.session.commit()

    return {"message": "Patient profile updated"}