from app.database.models import User, Role, UserRole, RefreshToken
from app.database.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.database.models import SystemRole
from flask_jwt_extended import  get_jwt_identity


def register_user(phone, password, role_name):
    if User.query.filter_by(phone=phone).first():
        return {"error": "User already exists"}, 400

    user = User(
        phone=phone,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.flush()

    if role_name not in [r.value for r in SystemRole]:
        return {"error": "Invalid role"}, 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return {"error": "Invalid role"}, 400

    db.session.add(UserRole(user_id=user.id, role_id=role.id))
    db.session.commit()

    return {"message": "User registered successfully"}, 201

def authenticate_user(phone, password):
    user = User.query.filter_by(phone = phone, is_active= True).first()
    if not user:
        return None
    if not check_password_hash(user.password_hash, password):
        return None
    return user

# def login_user(phone, password):
#     user = User.query.filter_by(phone=phone, is_active=True).first()
#     if not user:
#         return {"error": "Invalid credentials"}, 401

#     if not check_password_hash(user.password_hash, password):
#         return {"error": "Invalid credentials"}, 401

#     access_token = create_access_token(identity=user.id)
#     refresh_token = create_refresh_token(identity=user.id)

#     # print("uSER LOGIN SUCCESSFULL")
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token
#     }, 200

def logout_user():
    """
    Revoke the refresh token used for logout
    """
    user_id = int(get_jwt_identity())
    # jti = get_jwt()["jti"]

    token = RefreshToken.query.filter_by(
        user_id=user_id
        # token=jti,
        # revoked=False
    ).first()

    if not token:
        # token already revoked or invalid
        return {"message": "Already logged out"}, 200

    token.revoked = True
    db.session.commit()

    return {"message": "Logged out successfully"}, 200