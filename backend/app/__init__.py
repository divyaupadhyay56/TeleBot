from flask import Flask
from app.config import Config
from app.database.db import db
from app.database.models import seed_roles, RefreshToken
from app.routes.auth import auth_bp
from app.routes.doctors import doctor_bp
from app.routes.patients import patient_bp
from app.routes.hospitals import hospital_bp
from app.routes.pharmacies import pharmacy_bp
from app.routes.chatbot import chatbot_bp
from app.routes.appointments import appointments_bp
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
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(appointments_bp)
    return app
