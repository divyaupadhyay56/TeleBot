from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from app.database.models import UserRole, Role

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            role = (
                UserRole.query
                .join(Role)
                .filter(
                    UserRole.user_id == user_id,
                    Role.name == required_role
                )
                .first()
            )

            if not role:
                return {"error": "Unauthorized"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator