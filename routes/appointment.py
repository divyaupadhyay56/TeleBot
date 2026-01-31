from flask import Blueprint, request, jsonify
from TeleBot.models import db, Doctor, Appointment

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/doctors", methods=["GET"])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization
        }
        for d in doctors
    ])

@appointment_bp.route("/appointment", methods=["POST"])
def schedule_appointment():
    data = request.get_json()

    appt = Appointment(
        user_id=data["user_id"],          # ✅ NOW VALID
        doctor_id=data["doctor_id"],
        patient_name=data["patient_name"],
        time=data["time"]
    )

    db.session.add(appt)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Appointment scheduled successfully"
    })
