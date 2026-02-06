from flask import Blueprint, request
from app.services.auth_services import register_user, authenticate_user, logout_user
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    decode_token,
)
from datetime import datetime, timedelta
from app.database.db import db
from app.database.models import User, Role, UserRole, OTP, RefreshToken


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    phone = data["phone"]
    password = data["password"]
    role_name = data["role_name"]

    if not phone or not password or not role_name:
        return {"error": "Missing required fields"}, 400
    return register_user(phone, password, role_name)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    phone = data.get("phone")
    password = data.get("password")
    if isinstance(phone, (list, tuple)):
        phone = phone[0]
    # print(type(phone), phone)
    if not phone or not password:
        return {"error": "Missing credentials"}, 400

    user = authenticate_user(phone, password)
    if not user:
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    decoded = decode_token(refresh_token)
    # store fresh token
    db.session.add(
        RefreshToken(
            user_id=user.id,
            token=decoded["jti"],
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
    )
    db.session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}, 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    return logout_user()


@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    data = request.json

    contact = data.get("contact")  # phone or email
    purpose = data.get("purpose")  # login | reset | verify

    if not contact or not purpose:
        return {"error": "Missing fields"}, 400

    code = "123456"  # replace with random generator
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp = OTP(
        email=contact,
        code=code,
        purpose=purpose,
        expires_at=expires_at,
        resend_after=datetime.utcnow() + timedelta(seconds=60),
    )

    db.session.add(otp)
    db.session.commit()

    # send SMS/email here
    return {"message": "OTP sent"}, 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json

    contact = data.get("contact")
    code = data.get("code")
    purpose = data.get("purpose")

    otp = OTP.query.filter_by(email=contact, code=code, purpose=purpose).first()

    if not otp or otp.expires_at < datetime.utcnow():
        return {"error": "Invalid or expired OTP"}, 400

    # OTP valid → authorize action
    db.session.delete(otp)
    db.session.commit()

    return {"message": "OTP verified"}, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    roles = (
        db.session.query(Role.name)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    return {
        "id": user.id,
        "phone": user.phone,
        "roles": [r[0] for r in roles],
    }
