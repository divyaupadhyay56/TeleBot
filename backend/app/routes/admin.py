from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import User, UserRole, Role

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/me", methods=["GET"])
@jwt_required()
def get_admin_profile():
    user_id = get_jwt_identity()

    role = (
        UserRole.query
        .join(Role)
        .filter(
            UserRole.user_id == user_id,
            Role.name == "admin"
        )
        .first()
    )

    if not role:
        return {"error": "Admin access required"}, 403

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "phone": user.phone,
        "role": "admin",
        "created_at": user.created_at
    })
