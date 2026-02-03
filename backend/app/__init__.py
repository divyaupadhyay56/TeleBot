from flask import Flask
from app.config import Config
from app.database.db import db
from app.database.models import seed_roles, RefreshToken
from app.routes.auth import auth_bp
from app.routes.doctors import doctors_bp
from app.routes.patients import patients_bp
from app.routes.hospitals import hospitals_bp
from app.routes.pharmacies import pharmacies_bp
from flask_jwt_extended import JWTManager

jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RefreshToken.query.filter_by(token=jti, revoked=True).first()
    return token is not None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        seed_roles()

    app.register_blueprint(auth_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(pharmacies_bp)
    return app
