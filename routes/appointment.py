from flask import Blueprint, request, jsonify
from Chatbot.models import db, Doctor, Appointment

appointment_bp = Blueprint("appointment", __name__)

# ✅ List doctors (patient will choose)
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


# ✅ Schedule appointment
@appointment_bp.route("/appointment", methods=["POST"])
def schedule_appointment():
    try:
        data = request.get_json(force=True)

        user_id = str(data.get("user_id", "")).strip()
        doctor_id = data.get("doctor_id")
        date = str(data.get("date", "")).strip()
        time = str(data.get("time", "")).strip()
        reason = str(data.get("reason", "")).strip()

        if not user_id or not doctor_id or not date or not time:
            return jsonify({
                "status": "error",
                "message": "user_id, doctor_id, date, time are required"
            }), 400

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({"status": "error", "message": "Doctor not found"}), 404

        appt = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )

        db.session.add(appt)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Appointment scheduled successfully",
            "appointment": {
                "appointment_id": appt.id,
                "user_id": appt.user_id,
                "doctor": doctor.name,
                "specialization": doctor.specialization,
                "date": appt.date,
                "time": appt.time,
                "status": appt.status
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
