from flask import Blueprint, request, jsonify
from TeleBot.models import db, Doctor, Appointment

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/doctors", methods=["GET"])
def list_doctors():
    doctors = Doctor.query.all()
    return jsonify({
        "status": "success",
        "doctors": [
            {
                "id": d.id,
                "name": d.name,
                "specialization": d.specialization,
                "city": d.city,
                "contact": d.contact
            } for d in doctors
        ]
    })

@appointment_bp.route("/appointment", methods=["POST"])
def schedule_appointment():
    data = request.get_json(force=True)

    appt = Appointment(
        user_id=data.get("user_id"),
        doctor_id=data.get("doctor_id"),
        date=data.get("date"),
        time=data.get("time"),
        reason=data.get("reason")
    )

    db.session.add(appt)
    db.session.commit()

    return jsonify({"status": "success", "appointment_id": appt.id})
