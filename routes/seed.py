from flask import Blueprint, jsonify
from TeleBot.models import db, Doctor

seed_bp = Blueprint("seed", __name__)

@seed_bp.route("/seed-doctors", methods=["POST"])
def seed_doctors():
    if Doctor.query.count() > 0:
        return jsonify({"status": "success", "message": "Doctors already exist"}), 200

    doctors = [
        Doctor(name="Dr. Sharma", specialization="General Physician", city="Delhi", contact="9999999999"),
        Doctor(name="Dr. Verma", specialization="Dermatologist", city="Delhi", contact="8888888888"),
        Doctor(name="Dr. Khan", specialization="Cardiologist", city="Noida", contact="7777777777"),
    ]

    db.session.add_all(doctors)
    db.session.commit()

    return jsonify({"status": "success", "message": "Doctors inserted"})
